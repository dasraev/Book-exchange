from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
@shared_task
def send_password_reset_email(subject,message,to_email):
    # Your logic to send the password reset email
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [to_email],
        fail_silently=False,
    )
