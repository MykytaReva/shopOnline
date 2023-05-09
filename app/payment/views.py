import stripe

from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
from django.conf import settings

from cart.cart import CookiesCart
# from cart.models import Cart


# @login_required
def CartView(request):
    print(settings.STRIPE_PUBLISHABLE_KEY)
    cart = CookiesCart(request)
    total = str(cart.get_total_price())
    total = total.replace('.', '')
    total = int(total)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='gbp',
        metadata={'userid': request.user.id}
    )

    return render(
        request,
        'payment/home.html',
        {'client_secret': intent.client_secret}
        )
