from shop.models import Item

from .cart import CookiesCart
from .models import Cart


def cart_counter(request):
    if request.user.is_authenticated:
        # Get cart items for logged in user
        cart_items = Cart.objects.filter(user=request.user)
        cart_count = sum([it.quantity for it in cart_items])
    else:
        # Get cart items from session for anonymous user
        cart = CookiesCart(request)
        cart_items = []
        for item_id, item_data in cart.cart.items():
            item = Item.objects.get(pk=item_id)
            qty = item_data.get("qty")
            cart_items.append(
                {
                    "item": item,
                    "quantity": qty,
                }
            )
        cart_count = len(cart_items)
    return {"cart_count": cart_count}
