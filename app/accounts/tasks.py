from celery import shared_task
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model


@shared_task
def send_activation_email(user_pk):
    # get user model
    user = get_user_model().objects.get(pk=user_pk)
    # stable mail subject
    mail_subject = 'Please activate your account.'
    # email template depends on role
    if user.role == 1:
        email_template = 'emails/user_activation_email.html'
    elif user.role == 2:
        email_template = 'emails/shop_activation_email.html'

    current_site = 'localhost:8000'
    mail_subject = mail_subject
    message = render_to_string(email_template, {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user_pk)),
        'token': default_token_generator.make_token(user)
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, to=[to_email])
    mail.content_subtype = 'html'
    mail.send()


@shared_task
def print_every_2sec():
    print('NEXT PRINT WILL BE IN 1 minute')
