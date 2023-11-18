from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from .cart import CookiesCart
from .models import Cart


@receiver(user_logged_in)
def transfer_session_cart_to_database_cart(sender, request, user, **kwargs):
    # Check if there are any items in the session cart
    session_cart = CookiesCart(request)
    if session_cart.cart:
        # Transfer items from session cart to database cart
        for item_id, item_data in session_cart.cart.items():
            cart_item, created = Cart.objects.get_or_create(
                user=user,
                item_id=int(item_id),
            )
            if created:
                cart_item.quantity = item_data["qty"]
                cart_item.save()
        # Clear session cart
        session_cart.clear()
