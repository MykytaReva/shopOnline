from orders.models import ShopOrder, Shop


def get_new_orders_count(request):
    if request.user.is_authenticated and \
        request.user.is_staff and \
            not request.user.is_superuser:

        shop = Shop.objects.get(user=request.user)
        new_orders_count = ShopOrder.objects.filter(
                shop=shop,
                order__billing_status=True,
                status='New'
            ).count()
    else:
        new_orders_count = None

    return {'new_orders_count': new_orders_count}
