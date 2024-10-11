from django.core.mail import send_mail
from django.conf import settings

def login_handler_for_seller(user):
    if user.is_seller == True:
        return True
    return False

def is_user_verified(user):
    if user.is_verified == True:
        return True
    return False

def send_verification_email(message, email):
    send_mail(
        subject='Your verification email',
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )