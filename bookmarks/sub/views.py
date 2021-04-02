import stripe
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from sub.models import Subscription

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


class CheckoutSession(View):
    """ Subscription to Basic plan
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        YOUR_DOMAIN = 'http://127.0.0.1:8000/sub'

        checkout_session = stripe.checkout.Session.create(
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/canceled/',
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
            return_url='http://127.0.0.1:8000',
        )
        return redirect(session.url)


# WEBHOOKS
@csrf_exempt
def web_hooks(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
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
    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Fulfill the purchase
        fulfill_subscription(session)

    # Subscription updated
    elif event['type'] == 'customer.subscription.updated':
        session = event['data']['object']
        # Fulfill the purchase
        fulfill_subscription_update(session)

    # Subscription deleted
    elif event['type'] == 'customer.subscription.deleted':
        session = event['data']['object']
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
    print('Subscription created :::::::::', session)

    username = session['metadata']['username']
    customer = session['customer']
    customer_email = session['customer_details']['email']

    # Add stripe_id to user
    User.objects.filter(username=username).update(stripe_id=customer)

    # Add user to a group
    user = User.objects.get(username=username)
    group = Group.objects.get(name='subscribers')
    user.groups.add(group)

    # Add user billing info to Subscription model
    sub, created = Subscription.objects.update_or_create(user=user, defaults={
        'customer': customer,
        'customer_email': customer_email,
        'subscription': session['subscription'],
        'amount': session['amount_total'],
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
    print('Subscription updated :::::::', session)

    customer = session['customer']
    user = User.objects.get(stripe_id=customer)

    # Remove user from a group
    if session['status'] == 'canceled' or 'unpaid':
        group = Group.objects.get(name='subscribers')
        user.groups.remove(group)

    # Update user billing info in Subscription model
    sub, created = Subscription.objects.update_or_create(user=user, defaults={
        'customer': customer,
        'subscription': session['id'],
        'amount': session['plan']['amount'],
        'subscription_status': session['status'],
    })

    send_mail(
        subject='Customer’s payment succeeded',
        # message=f'Thanks for you donation. Here is your product {product.url}',
        message=f'Your subscription has been update or cancelled...',
        recipient_list=[user.email],
        from_email=settings.EMAIL_HOST_USER
    )
