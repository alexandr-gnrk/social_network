from time import sleep

from celery import shared_task
from django.core.mail import send_mass_mail


@shared_task
def send_mail_task(*args, **kwargs):
    # sleep(30)
    send_mass_mail(*args, **kwargs)
    return None
