from django.http.response import JsonResponse

from cart.cart import CookiesCart
from .models import Order, OrderItem


def add(request):
    cart = CookiesCart(request)
    cart_items = cart.get_items()
    if request.POST.get('action') == 'post':

        # user_id = request.user.id
        user_id = 2
        order_key = request.POST.get('order_key')
        carttotal = cart.get_total_price()

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
            for item in cart_items:
                OrderItem.objects.create(
                    order_id=order_id,
                    item=item['item'],
                    price=item['item'].price,
                    quantity=item['quantity']
                )
        response = JsonResponse({'success': 'Return something'})
        return response


def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)
