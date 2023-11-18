from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from django.views.generic.base import View
from shop.models import Item

from .cart import CookiesCart
from .models import Cart


class AddToCartView(View):
    """
    Add an item to the cart
    """

    def post(self, request, *args, **kwargs):
        item = get_object_or_404(Item, pk=self.kwargs["pk"])
        if request.user.is_authenticated:
            cart_item, created = Cart.objects.get_or_create(user=request.user, item=item)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
            return JsonResponse(
                {
                    "message": "Added to the Cart!",
                    "icon": "success",
                }
            )
        else:
            cart = CookiesCart(request)
            cart.add(item)
            return JsonResponse(
                {
                    "message": "Added to the Cart!",
                    "icon": "success",
                }
            )


class SubtractFromCartView(View):
    def post(self, request, *args, **kwargs):
        item = get_object_or_404(Item, id=self.kwargs["pk"])

        if request.user.is_authenticated:
            cart_item = get_object_or_404(Cart, user=request.user, item=item)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        else:
            cart = CookiesCart(request)
            cart.subtract(item)

        return JsonResponse(
            {
                "message": "Removed from the Cart!",
                "icon": "warning",
            }
        )


class RemoveFromCartView(View):
    def post(self, request, *args, **kwargs):
        item = get_object_or_404(Item, id=self.kwargs["pk"])

        if request.user.is_authenticated:
            cart_item = get_object_or_404(Cart, user=request.user, item=item)
            cart_item.delete()
        else:
            cart = CookiesCart(request)
            cart.delete(item)

        return JsonResponse(
            {
                "message": "Deleted from the Cart!",
                "icon": "warning",
            }
        )


class CartView(generic.TemplateView):
    template_name = "marketplace/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Get cart items for logged in user
            cart_items = Cart.objects.filter(user=self.request.user).order_by("created_at")
            cart_count = sum([it.quantity for it in cart_items])
            context["cart_counter"] = cart_count
            context["total"] = sum([it.quantity * it.item.price for it in cart_items])
        else:
            # Get cart items from session for anonymous user
            cart = CookiesCart(self.request)
            cart_items = cart.get_items()
            cart_count = len(cart_items)

            context["total"] = cart.get_total_price()

        context["cart_items"] = cart_items
        context["cart_counter"] = cart_count

        return context
