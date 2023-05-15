from django.db import models
from django.contrib.auth import get_user_model

from shop.models import Item, Shop


class Order(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='order_user',
    )
    shops = models.ManyToManyField(Shop, blank=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=14, blank=True)

    address = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=16, blank=True, null=True)
    city = models.CharField(max_length=16, blank=True, null=True)
    state = models.CharField(max_length=40, blank=True, null=True)
    pin_code = models.CharField(max_length=15, blank=True, null=True)

    billing_status = models.BooleanField(default=False)
    order_key = models.CharField(max_length=200)
    total_paid = models.DecimalField(max_digits=7, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.created_at)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    item = models.ForeignKey(
        Item,
        related_name='order_items',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
