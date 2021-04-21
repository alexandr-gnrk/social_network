from django.contrib import admin

from sub.models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'customer_email', 'subscription', 'amount', 'subscription_status']
