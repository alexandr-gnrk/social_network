from django.urls import path

from .views import CheckoutSession, CheckoutSessionSuccess, CheckoutSessionCanceled, CustomerPortal, web_hooks, \
    CheckoutSessionView, CustomerPortalView

app_name = 'sub'

urlpatterns = [
    path('create-checkout-session/', CheckoutSession.as_view(), name='create-checkout-session'),
    path('success/', CheckoutSessionSuccess.as_view(), name='success'),
    path('canceled/', CheckoutSessionCanceled.as_view(), name='cancel'),
    path('create-customer-portal-session/', CustomerPortal.as_view(), name='create-customer-portal-session'),
    path('webhooks/', web_hooks, name='webhooks'),

    path('api/create-checkout-session/', CheckoutSessionView.as_view()),
    path('api/create-customer-portal-session/', CustomerPortalView.as_view()),
]
