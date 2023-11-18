import json

import stripe
from cart.models import Cart
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from orders.models import Order
from orders.views import payment_confirmation


class CartView(LoginRequiredMixin, TemplateView):
    template_name = "payment/home.html"

    def get(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=self.request.user).order_by("created_at")
        total = sum([it.quantity * it.item.price for it in cart_items])
        total = int(total * 100)

        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            intent = stripe.PaymentIntent.create(amount=total, currency="gbp", metadata={"userid": 2})
        except stripe.error.StripeError as e:
            # Handle payment error
            error_message = str(e)
            return render(request, self.template_name, {"error_message": error_message})
        except stripe.error.CardError as e:
            # Display error message to the user
            err = e.error
            return render(request, self.template_name, {"error": err["message"]})

        return render(
            request,
            self.template_name,
            {
                "client_secret": intent.client_secret,
                "total": total / 100,
            },
        )


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(json.loads(payload), stripe.api_key)
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == "payment_intent.succeeded":
        payment_confirmation(event.data.object.client_secret)
    else:
        print("Unhandled event type{}".format(event.type))

    return HttpResponse(status=200)


def order_placed(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    order = Order.objects.filter(user=user).first()
    context = {
        "user": user,
        "order": order,
        "orderitems": order.items.all(),
        "total": order.total_paid,
    }
    cart.delete()
    return render(request, "payment/orderplaced.html", context=context)
