from django.db.models.signals import pre_save
from django.dispatch import receiver

from orders.models import ShopOrder
from accounts.tasks import send_status_in_process, send_status_sent


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
