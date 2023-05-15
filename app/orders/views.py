from django.http.response import JsonResponse
from django.contrib import messages

from .models import Order, OrderItem
from cart.models import Cart


def add(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)

    if request.POST.get('action') == 'post':
        user_id = user.id
        order_key = request.POST.get('order_key')
        carttotal = sum(
                [it.quantity*it.item.price for it in cart_items]
                )

        # check if order already exists
        if not Order.objects.filter(order_key=order_key).exists():
            order = Order.objects.create(
                user_id=user_id,
                first_name='first_name',
                last_name='last_name',
                phone_number='phone_number',


                address='address',
                country='country',
                city='city',
                state='state',
                pin_code='zip_code',

                total_paid=carttotal,
                order_key=order_key
            )

            order_id = order.pk
            added_shops = set()
            for item in cart_items:
                shop = item.item.shop
                if shop not in added_shops:
                    order.shops.add(shop)
                    added_shops.add(shop)

                OrderItem.objects.create(
                    order_id=order_id,
                    item=item.item,
                    price=item.item.price,
                    quantity=item.quantity,
                )

        response = JsonResponse({'success': 'Return something'})
        messages.success(request, 'Order successfully placed!')
        return response


def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)
