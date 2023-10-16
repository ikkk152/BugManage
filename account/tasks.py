from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_mail_task(username, mobile, email):
    send_mail(
        settings.SUBJECT,
        settings.MESSAGE_TEMPLATE % (username, mobile),
        settings.EMAIL_HOST_USER,
        [email, ]
    )
