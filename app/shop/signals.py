from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Shop, Item
from orders.models import ShopOrder
from accounts.tasks import (
    send_status_in_process,
    send_status_sent,
    send_shop_is_confirmed_email,
    send_item_is_confirmed_email,
)


@receiver(pre_save, sender=ShopOrder)
def post_save_status_update(sender, instance, **kwargs):
    try:

        old_status = ShopOrder.objects.get(pk=instance.pk).status
        new_status = instance.status

        if new_status != old_status:
            if new_status == 'In Process':
                send_status_in_process.delay(instance.pk)
                # print('send_status_in_process.delay()')
            elif new_status == 'Sent':
                send_status_sent.delay(instance.pk)
                # print('send_status_sent.delay()')
    except:
        pass


@receiver(pre_save, sender=Shop)
def pre_save_create_profile_receiver(sender, instance, **kwargs):
    try:

        old_status = Shop.objects.get(pk=instance.pk).is_approved
        new_status = instance.is_approved

        if new_status != old_status:
            if new_status:
                send_shop_is_confirmed_email.delay(instance.pk)
    except:
        pass


@receiver(pre_save, sender=Item)
def pre_save_create_item_receiver(sender, instance, **kwargs):
    try:

        old_status = Item.objects.get(pk=instance.pk).is_approved
        new_status = instance.is_approved

        if new_status != old_status:
            if new_status:
                print('send_item_is_confirmed_email.delay(instance.pk)')
                send_item_is_confirmed_email.delay(instance.pk)
    except:
        pass
