import json

import stripe
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from sub.models import Subscription

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


class Sub(View):
    """ Подписка на своем сайте
        Работет для страйпового кастомера с добавленой картой. Не работет для юзера
    """
    def post(self, request, *args, **kwargs):
        try:
            # token = request.POST.get('stripeToken')
            customer = stripe.Customer.create(
                email=request.user.email,
                name=request.user.username,
                source="tok_visa",
                # default_payment_method=
                # source=token
                # payment_method=,
                # payment_method_types=['card']
                # source=request.POST['stripeToken']
            )
            subscription = stripe.Subscription.create(
                # customer='cus_JBK9ZWUTmfRBEp',
                customer=customer['id'],
                items=[
                    {
                        'price': 'price_1IYxwmIBBCpvms2A4iYflBa2',
                        'quantity': 1,
                    },
                ],
            )
            # print('++++++++++++', subscription)

            return JsonResponse({
                'id': subscription.id
            })

        except Exception as e:
            JsonResponse({'error': str(e)})


class Index(TemplateView):
    template_name = 'sub/sub.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'STRIPE_TEST_PUBLISHABLE_KEY': settings.STRIPE_TEST_PUBLISHABLE_KEY
        })
        return context


# =====================================================
# Subscription and Billing portal with Stripe Session
# =====================================================

class SubSession(View):
    """ Subscribe Session
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        YOUR_DOMAIN = 'http://127.0.0.1:8000/sub'

        checkout_session = stripe.checkout.Session.create(
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
            payment_method_types=['card'],
            line_items=[
                {
                    'price': 'price_1IYdWTIBBCpvms2AD3uN9D9f',
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


class Success(TemplateView):
    template_name = 'sub/success.html'


class Cancel(TemplateView):
    template_name = 'sub/cancel.html'


class Session(TemplateView):
    template_name = 'sub/session.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'STRIPE_TEST_PUBLISHABLE_KEY': settings.STRIPE_TEST_PUBLISHABLE_KEY
        })
        return context


class Portal(View):
    """ Billing portal
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        customer = user.stripe_id

        # if not customer:
        #     customer = stripe.Customer.create(
        #         email=request.user.email,
        #         name=request.user.username,
        #     )
        #     customer = customer['id']
        #     user.stripe_id = customer
        #     user.save()

        # Authenticate your user.
        session = stripe.billing_portal.Session.create(
            customer=customer,
            return_url='http://127.0.0.1:8000',
        )
        # print(session)
        return redirect(session.url)


# ==================================================================
# Web hooks
# ==================================================================

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

    # Subscription updated, deleted (pause: "pause_collection":{})
    elif event['type'] == 'customer.subscription.deleted' or 'customer.subscription.updated':
        session = event['data']['object']  # contains a stripe.PaymentIntent
        # Fulfill the purchase
        fulfill_subscription_update(session)

    # Subscription pause
    # customer.subscription.updated

    # elif event['type'] == 'payment_intent.succeeded':
    #     # 4242424242424242	Successful payment
    #
    # elif event['type'] == 'payment_intent.payment_failed':
    #     # 4000000000000002	Charge is declined with a card_declined code.
    #     # 4000000000000069	Charge is declined with an expired_card code.
    #

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_subscription(session):
    """ Subscription created
    """
    # print('Subscription created :::::::::', session)

    username = session['metadata']['username']
    customer = session['customer']
    customer_email = session['customer_details']['email']

    # user, created = User.objects.update_or_create(username=username, defaults={
    #     'stripe_id': customer_id,
    #     'is_staff': True,
    #     # 'stripe_sub': subscription_id,
    # })
    # User.objects.filter(username=username).update(stripe_id=customer, is_staff=True)
    User.objects.filter(username=username).update(stripe_id=customer)

    user = User.objects.get(username=username)
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
    print('Subscription deleted :::::::', session)
    customer = session['customer']
    user = User.objects.get(stripe_id=customer)

    sub, created = Subscription.objects.update_or_create(user=user, defaults={
        'customer': customer,
        'subscription': session['id'],
        'amount': session['plan']['amount'],
        'subscription_status': session['status'],
    })


# ==================================================================
# Create Payment Intent
# ==================================================================
#
# class CreatePaymentIntentView(View):
#     def post(self, request, *args, **kwargs):
#         user = request.user
#         customer = stripe.Customer.create(email=user.email)
#
#         try:
#             product_id = self.kwargs['pk']
#             product = Product.objects.get(id=product_id)
#             intent = stripe.PaymentIntent.create(
#                 customer=customer['id'],
#                 setup_future_usage='off_session',
#                 amount=product.price,
#                 currency='usd',
#                 metadata={
#                     'product_id': product.id,
#                     'user': user,
#                     'user_username': user.username,
#                     'user_email': user.email,
#                     'user_paid_until': user.paid_until,
#                     'user_has_paid': user.has_paid,
#                 },
#             )
#             return JsonResponse({
#                 'clientSecret': intent['client_secret']
#             })
#         except Exception as e:
#             JsonResponse({'error': str(e)})
#
#
# class CheckoutIntentView(TemplateView):
#     template_name = 'payments/checkout_intent.html'
#
#     def get_context_data(self, **kwargs):
#         product = Product.objects.get(name='Basic')
#         context = super(CheckoutIntentView, self).get_context_data(**kwargs)
#         context.update({
#             'product': product,
#             'STRIPE_TEST_PUBLISHABLE_KEY': settings.STRIPE_TEST_PUBLISHABLE_KEY
#         })
#         return context


# # Get the permission
# permission = Permission.objects.get(codename='special_status')
#
# # Get user
# u = request.user
#
# # Add to user's permission set
# u.user_permissions.add(permission)
