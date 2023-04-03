from celery import shared_task


@shared_task
def send_activation_email(user_pk):
    # from django.contrib.sites.shortcuts import get_current_site
    from django.template.loader import render_to_string
    from django.utils.http import urlsafe_base64_encode
    from django.utils.encoding import force_bytes
    from django.contrib.auth.tokens import default_token_generator
    from django.core.mail import EmailMessage
    from django.contrib.auth import get_user_model
    # from django.contrib.sites.models import Site

    # get user model
    user = get_user_model().objects.get(pk=user_pk)
    # stable mail subject
    mail_subject = 'Please activate your account.'
    # email template depends on role
    if user.role == 1:
        email_template = 'emails/user_activation_email.html'
    elif user.role == 2:
        email_template = 'emails/shop_activation_email.html'

    # current_site = Site.objects.get_current().domain
    current_site = 'localhost'
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
    print('EMAIL SENT NOT YET SENT')
    mail.send()
    print('EMAIL SENT')


@shared_task
def slow_func():
    from time import sleep
    print('start')
    sleep(10)
    print('end')


# from django.core.mail import send_mail

# @shared_task
# def send_email_activation(user, mail_subject, email_template):
#     current_site = 'localhost'
#     mail_subject = mail_subject
#     message = render_to_string(email_template, {
#         'user': user,
#         'domain': current_site,
#         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#         'token': default_token_generator.make_token(user),
#     })

#     send_mail(
#         mail_subject,
#         message,
#         user.email,
#         settings.EMAIL_HOST_USER,
#         fail_silently=False,
#     )
