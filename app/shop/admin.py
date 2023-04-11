from django.contrib import admin
from .models import Shop, Item, Category, ItemImage

admin.site.register(Shop)
admin.site.register(Item)
admin.site.register(ItemImage)
admin.site.register(Category)
