from django.contrib.auth.models import User
from django.db import models


class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stripe')
    customer = models.CharField(max_length=200, blank=True, null=True)
    customer_email = models.EmailField(blank=True, null=True)
    subscription = models.CharField(max_length=200, blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    subscription_status = models.CharField(max_length=50, blank=True, null=True)


