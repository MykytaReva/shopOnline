from django.db import models

from shop.models import Item
from django.contrib.auth import get_user_model


class Cart(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='cart_items',
        )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='cart_items'
        )
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.item.name
