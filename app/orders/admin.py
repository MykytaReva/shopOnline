from django.contrib import admin
from .models import Order, OrderItem, ShopOrder

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShopOrder)
