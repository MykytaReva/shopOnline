from django.contrib import admin

from .models import Category, Item, ItemImage, Shop

admin.site.register(Shop)
admin.site.register(Item)
admin.site.register(ItemImage)
admin.site.register(Category)
