from celery import shared_task
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model

from .models import DailyLetter
from orders.models import ShopOrder, Order
from shop.models import Shop, Item


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

    current_site = '127.0.0.1:8000'
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
def send_verification_email(user_pk):
    # get user model
    user = get_user_model().objects.get(pk=user_pk)
    # stable mail subject
    mail_subject = 'Reset your password.'
    email_template = 'emails/user_reset_email.html'
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
def send_daily_newsletter():
    # Get queryset of email addresses from the model
    receivers = DailyLetter.objects.all()

    # Extract the email addresses from queryset
    to_emails = list(receivers.values_list('email', flat=True))

    # Compose email message
    subject = 'Daily Newsletter'
    body = 'Hello,\n\nHere is your daily newsletter.'

    message = EmailMessage(subject, body, to=to_emails)
    message.content_subtype = 'html'

    message.send()


@shared_task
def send_status_in_process(instance_pk):
    shop = ShopOrder.objects.get(pk=instance_pk)
    user = shop.order.user
    to_email = user.email

    email_template = 'emails/send_status_in_process.html'

    subject = 'Order Status Changed'
    message = render_to_string(email_template, {
        'user': user,
    })
    mail = EmailMessage(subject, message, to=[to_email])
    mail.content_subtype = 'html'
    mail.send()


@shared_task
def send_status_sent(instance_pk):
    shop = ShopOrder.objects.get(pk=instance_pk)
    user = shop.order.user
    to_email = user.email

    email_template = 'emails/send_status_sent.html'

    subject = 'Order Status Changed'
    message = render_to_string(email_template, {
        'user': user,
    })
    mail = EmailMessage(subject, message, to=[to_email])
    mail.content_subtype = 'html'
    mail.send()


@shared_task
def new_order_notification(order_pk):

    order = Order.objects.get(pk=order_pk)
    order_items = order.items.all()

    to_emails = list(
        {order_item.item.shop.user.email for order_item in order_items}
        )

    subject = 'New Order Notification'
    body = 'Hello,you have a new order!'

    message = EmailMessage(subject, body, to=to_emails)
    message.content_subtype = 'html'

    message.send()


@shared_task
def send_order_confirmation(order_pk):

    order = Order.objects.get(pk=order_pk)
    user = order.user
    to_email = user.email

    email_template = 'emails/order_confirmation.html'

    subject = 'Your order information.'
    message = render_to_string(email_template, {
        'user': user,
    })
    mail = EmailMessage(subject, message, to=[to_email])
    mail.content_subtype = 'html'
    mail.send()


@shared_task
def send_shop_is_confirmed_email(shop_pk):

    shop = Shop.objects.get(pk=shop_pk)
    user = shop.user
    to_email = user.email

    email_template = 'emails/shop_is_approved.html'

    subject = 'Your shop is approved!'
    message = render_to_string(email_template, {
        'user': user,
    })
    mail = EmailMessage(subject, message, to=[to_email])
    mail.content_subtype = 'html'
    mail.send()


@shared_task
def send_item_is_confirmed_email(shop_pk):

    item = Item.objects.get(pk=shop_pk)
    user = item.shop.user
    to_email = user.email

    email_template = 'emails/shop_item_is_approved.html'

    subject = 'Your Product has been approved!'
    message = render_to_string(email_template, {
        'user': user,
    })
    mail = EmailMessage(subject, message, to=[to_email])
    mail.content_subtype = 'html'
    mail.send()
