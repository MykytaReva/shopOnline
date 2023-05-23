from django.http.response import JsonResponse
from django.contrib import messages

from .models import Order, OrderItem, ShopOrder
from cart.models import Cart
from accounts.tasks import new_order_notification, send_order_confirmation


def add(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)

    if request.POST.get('action') == 'post':
        user_id = user.id
        order_key = request.POST.get('order_key')
        carttotal = sum(
                [it.quantity*it.item.price for it in cart_items]
                )
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        email_address = request.user.email
        address = request.POST.get('address')
        state = request.POST.get('state')
        city = request.POST.get('city')
        pin_code = request.POST.get('pin_code')
        country = request.POST.get('country')

        # check if order already exists
        if not Order.objects.filter(order_key=order_key).exists():
            order = Order.objects.create(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,


                address=address,
                country=country,
                city=city,
                state=state,
                pin_code=pin_code,

                total_paid=carttotal,
                order_key=order_key
            )
            # create order items
            order_id = order.pk
            for item in cart_items:
                shop = item.item.shop
                OrderItem.objects.create(
                    order_id=order_id,
                    item=item.item,
                    price=item.item.price,
                    quantity=item.quantity,
                )
                shop_order, created = ShopOrder.objects.get_or_create(
                    shop=shop,
                    order=order,
                )
                if not created:
                    shop_order.save()

        response = JsonResponse({'success': 'Return something'})
        messages.success(request, 'Order successfully placed!')
        return response


def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)
    order = Order.objects.get(order_key=data)
    # email to all shops in the order
    new_order_notification.delay(order.pk)
    # email to the user
    send_order_confirmation.delay(order.pk)
