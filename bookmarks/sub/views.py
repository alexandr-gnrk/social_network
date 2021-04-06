from urllib.parse import urljoin

import stripe
from decouple import config
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from account.tasks import send_mail_task
from sub.models import Subscription

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
domain = settings.STRIPE_SITE_URL


class CheckoutSession(View):
    """ Subscription to Basic plan
    """
    def post(self, request, *args, **kwargs):
        user = request.user

        checkout_session = stripe.checkout.Session.create(
            success_url=urljoin(domain, 'sub/success'),
            cancel_url=urljoin(domain, 'sub/canceled'),
            payment_method_types=['card'],
            line_items=[
                {
                    'price': settings.STRIPE_PLAN_BASIC_ID,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            metadata={
                'username': user.username,
                'user_email': user.email,
            },
        )

        return JsonResponse({
            'id': checkout_session.id
        })


class CheckoutSessionSuccess(TemplateView):
    template_name = 'sub/success.html'


class CheckoutSessionCanceled(TemplateView):
    template_name = 'sub/canceled.html'


class CustomerPortal(View):
    """ Manage billing
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        customer = user.stripe_id

        # Authenticate your user.
        session = stripe.billing_portal.Session.create(
            customer=customer,
            return_url=domain
        )
        return redirect(session.url)


# WEBHOOKS
@csrf_exempt
def web_hooks(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Subscription created
    if event.get('type') == 'checkout.session.completed':
        # session = event['data']['object']
        session = event.get('data', {}).get('object')
        # Fulfill the purchase
        fulfill_subscription(session)

    # Subscription updated
    elif event.get('type') == 'customer.subscription.updated':
        session = event.get('data', {}).get('object')
        # Fulfill the purchase
        fulfill_subscription_update(session)

    # Subscription deleted
    elif event.get('type') == 'customer.subscription.deleted':
        session = event.get('data', {}).get('object')
        # Fulfill the purchase
        fulfill_subscription_update(session)

    # If subscription collection_method=charge_automatically it becomes past_due
    # when payment to renew it fails and canceled or unpaid (depending on your subscriptions settings)
    # when Stripe has exhausted all payment retry attempts.

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_subscription(session):
    """ Subscription created
    """
    username = session.get('metadata', {}).get('username')
    customer = session.get('customer')
    customer_email = session.get('customer_details', {}).get('email')

    # Add stripe_id to user
    User.objects.filter(username=username).update(stripe_id=customer)

    # Add user to a group
    user = User.objects.get(username=username)
    group = get_object_or_404(Group, name='subscribers')
    user.groups.add(group)

    # Add user billing info to Subscription model
    sub, created = Subscription.objects.update_or_create(user=user, defaults={
        'customer': customer,
        'customer_email': customer_email,
        'subscription': session.get('subscription'),
        'amount': session.get('amount_total'),
        'subscription_status': 'active',
    })

    send_mail(
        subject='Customer’s payment succeeded',
        # message=f'Thanks for you donation. Here is your product {product.url}',
        message=f'Thanks for you donation. Here is your product...',
        recipient_list=[customer_email],
        from_email=settings.EMAIL_HOST_USER
    )


def fulfill_subscription_update(session):
    """ Subscription updated, deleted
    """
    customer = session.get('customer')
    user = User.objects.get(stripe_id=customer)

    # Remove user from a group
    if session.get('status') in ('canceled', 'unpaid'):
        group = get_object_or_404(Group, name='subscribers')
        user.groups.remove(group)

    # Update user billing info in Subscription model
    sub, created = Subscription.objects.update_or_create(user=user, defaults={
        'customer': customer,
        'subscription': session.get('id'),
        'amount': session.get('plan', {}).get('amount'),
        'subscription_status': session.get('status'),
    })

    # Send mail
    subject = 'Customer’s payment succeeded'
    text = f'Your subscription has been update or cancelled...'
    sender = config('EMAIL_HOST_USER')
    message = (subject, text, sender, [user.email])
    send_mail_task.delay((message,), fail_silently=False)

