import stripe
import json

from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from orders.views import payment_confirmation
from cart.models import Cart
from cart.cart import CookiesCart


class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'payment/home.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            cart_items = Cart.objects.filter(
                user=self.request.user
                ).order_by('created_at')
            total = sum(
                [it.quantity*it.item.price for it in cart_items]
                )
            total = int(total * 100)
        else:
            cart = CookiesCart(self.request)
            total = str(cart.get_total_price())
            total = total.replace('.', '')
            total = int(total)

        stripe.api_key = settings.STRIPE_SECRET_KEY

        intent = stripe.PaymentIntent.create(
            amount=total,
            currency='gbp',
            metadata={'userid': 2}
        )

        return render(
            request,
            self.template_name,
            {'client_secret': intent.client_secret}
        )


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)
    else:
        print('Unhandled event type{}'.format(event.type))

    return HttpResponse(status=200)


def order_placed(request):
    Cart.objects.filter(
                user=request.user
                ).delete()
    return render(request, 'payment/orderplaced.html')
