import logging

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from orders.models import Order, ShopOrder
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from shop.models import Item, Shop

from .models import DailyLetter


@shared_task
def send_activation_email(user_pk):
    user = get_user_model().objects.get(pk=user_pk)
    mail_subject = "Please activate your account."
    to_email = user.email
    # email template depends on role
    if user.role == 2:
        email_template = "emails/shop_activation_email.html"
    else:
        email_template = "emails/user_activation_email.html"

    message = render_to_string(
        email_template,
        {
            "user": user,
            "domain": settings.ALLOWED_HOSTS[0],
            "uid": urlsafe_base64_encode(force_bytes(user_pk)),
            "token": default_token_generator.make_token(user),
        },
    )
    try:
        sendgrid_api_key = settings.SENDGRID_API_KEY
        if not sendgrid_api_key:
            raise Exception("SendGrid API key is missing")

        sg = SendGridAPIClient(sendgrid_api_key)
        message = Mail(from_email=settings.FROM_EMAIL, to_emails=to_email, subject=mail_subject, html_content=message)
        logging.info(f"Email sent in {settings.ENV} environment.")
        sg.send(message)

    except Exception as e:
        logging.error("An error occurred:", str(e))


@shared_task
def send_verification_email(user_pk):
    # get user model
    user = get_user_model().objects.get(pk=user_pk)
    # stable mail subject
    mail_subject = "Reset your password."
    email_template = "emails/user_reset_email.html"

    message = render_to_string(
        email_template,
        {
            "user": user,
            "domain": settings.ALLOWED_HOSTS[0],
            "uid": urlsafe_base64_encode(force_bytes(user_pk)),
            "token": default_token_generator.make_token(user),
        },
    )
    to_email = user.email
    try:
        sendgrid_api_key = settings.SENDGRID_API_KEY
        if not sendgrid_api_key:
            raise Exception("SendGrid API key is missing")
        sg = SendGridAPIClient(sendgrid_api_key)
        message = Mail(from_email=settings.FROM_EMAIL, to_emails=to_email, subject=mail_subject, html_content=message)
        logging.info(f"Email sent in {settings.ENV} environment.")
        sg.send(message)
    except Exception as e:
        logging.error("An error occurred:", str(e))


@shared_task
def send_daily_newsletter():
    # Get queryset of email addresses from the model
    receivers = DailyLetter.objects.all()

    # Extract the email addresses from queryset
    to_emails = list(receivers.values_list("email", flat=True))

    # Compose email message
    subject = "Daily Newsletter"
    body = "Hello,\n\nHere is your daily newsletter."
    try:
        sendgrid_api_key = settings.SENDGRID_API_KEY
        if not sendgrid_api_key:
            raise Exception("SendGrid API key is missing")
        sg = SendGridAPIClient(sendgrid_api_key)
        message = Mail(
            from_email=settings.FROM_EMAIL, to_emails=to_email, subject=mail_subject, plain_text_content=body
        )
        logging.info(f"Email sent in {settings.ENV} environment.")
        sg.send(message)
    except Exception as e:
        logging.error("An error occurred:", str(e))


@shared_task
def send_status_in_process(instance_pk):
    shop = ShopOrder.objects.get(pk=instance_pk)
    user = shop.order.user
    to_email = user.email

    email_template = "emails/send_status_in_process.html"

    subject = "Order Status Changed"
    message = render_to_string(
        email_template,
        {
            "user": user,
        },
    )
    try:
        sendgrid_api_key = settings.SENDGRID_API_KEY
        if not sendgrid_api_key:
            raise Exception("SendGrid API key is missing")
        sg = SendGridAPIClient(sendgrid_api_key)
        message = Mail(from_email=settings.FROM_EMAIL, to_emails=to_email, subject=mail_subject, html_content=message)
        logging.info(f"Email sent in {settings.ENV} environment.")
        sg.send(message)
    except Exception as e:
        logging.error("An error occurred:", str(e))


@shared_task
def send_status_sent(instance_pk):
    shop = ShopOrder.objects.get(pk=instance_pk)
    user = shop.order.user
    to_email = user.email

    email_template = "emails/send_status_sent.html"

    subject = "Order Status Changed"
    message = render_to_string(
        email_template,
        {
            "user": user,
        },
    )
    try:
        sendgrid_api_key = settings.SENDGRID_API_KEY
        if not sendgrid_api_key:
            raise Exception("SendGrid API key is missing")
        sg = SendGridAPIClient(sendgrid_api_key)
        message = Mail(from_email=settings.FROM_EMAIL, to_emails=to_email, subject=mail_subject, html_content=message)
        logging.info(f"Email sent in {settings.ENV} environment.")
        sg.send(message)
    except Exception as e:
        logging.error("An error occurred:", str(e))


@shared_task
def new_order_notification(order_pk):

    order = Order.objects.get(pk=order_pk)
    order_items = order.items.all()

    to_emails = list({order_item.item.shop.user.email for order_item in order_items})

    subject = "New Order Notification"
    body = "Hello,you have a new order!"
    try:
        sendgrid_api_key = settings.SENDGRID_API_KEY
        if not sendgrid_api_key:
            raise Exception("SendGrid API key is missing")
        sg = SendGridAPIClient(sendgrid_api_key)
        message = Mail(
            from_email=settings.FROM_EMAIL, to_emails=to_email, subject=mail_subject, plain_text_content=body
        )
        logging.info(f"Email sent in {settings.ENV} environment.")
        sg.send(message)
    except Exception as e:
        logging.error("An error occurred:", str(e))


@shared_task
def send_order_confirmation(order_pk):

    order = Order.objects.get(pk=order_pk)
    user = order.user
    to_email = user.email

    email_template = "emails/order_confirmation.html"

    subject = "Your order information."
    message = render_to_string(
        email_template,
        {
            "user": user,
        },
    )
    try:
        sendgrid_api_key = settings.SENDGRID_API_KEY
        if not sendgrid_api_key:
            raise Exception("SendGrid API key is missing")
        sg = SendGridAPIClient(sendgrid_api_key)
        message = Mail(from_email=settings.FROM_EMAIL, to_emails=to_email, subject=mail_subject, html_content=message)
        logging.info(f"Email sent in {settings.ENV} environment.")
        sg.send(message)
    except Exception as e:
        logging.error("An error occurred:", str(e))


@shared_task
def send_shop_is_confirmed_email(shop_pk):

    shop = Shop.objects.get(pk=shop_pk)
    user = shop.user
    to_email = user.email

    email_template = "emails/shop_is_approved.html"

    subject = "Your shop is approved!"
    message = render_to_string(
        email_template,
        {
            "user": user,
        },
    )
    try:
        sendgrid_api_key = settings.SENDGRID_API_KEY
        if not sendgrid_api_key:
            raise Exception("SendGrid API key is missing")
        sg = SendGridAPIClient(sendgrid_api_key)
        message = Mail(from_email=settings.FROM_EMAIL, to_emails=to_email, subject=mail_subject, html_content=message)
        logging.info(f"Email sent in {settings.ENV} environment.")
        sg.send(message)
    except Exception as e:
        logging.error("An error occurred:", str(e))


@shared_task
def send_item_is_confirmed_email(shop_pk):

    item = Item.objects.get(pk=shop_pk)
    user = item.shop.user
    to_email = user.email

    email_template = "emails/shop_item_is_approved.html"

    subject = "Your Product has been approved!"
    message = render_to_string(
        email_template,
        {
            "user": user,
        },
    )
    try:
        sendgrid_api_key = settings.SENDGRID_API_KEY
        if not sendgrid_api_key:
            raise Exception("SendGrid API key is missing")
        sg = SendGridAPIClient(sendgrid_api_key)
        message = Mail(from_email=settings.FROM_EMAIL, to_emails=to_email, subject=mail_subject, html_content=message)
        logging.info(f"Email sent in {settings.ENV} environment.")
        sg.send(message)
    except Exception as e:
        logging.error("An error occurred:", str(e))
