from orders.models import Item, Shop, ShopOrder


def get_new_orders_count(request):
    if request.user.is_authenticated and request.user.is_staff and not request.user.is_superuser:

        shop = Shop.objects.get(user=request.user)
        new_orders_count = ShopOrder.objects.filter(shop=shop, order__billing_status=True, status="New").count()
    else:
        new_orders_count = None

    return {"new_orders_count": new_orders_count}


def get_not_approved_numbers(request):
    if request.user.is_superuser:
        shops = Shop.objects.filter(is_approved=False)
        items = Item.objects.filter(is_approved=False)
        new_shops = shops.count()
        new_items = items.count()

    else:
        new_shops, new_items = None, None
    return {"new_shops": new_shops, "new_items": new_items}
