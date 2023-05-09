from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path(
        'add-to-cart/<int:pk>/',
        views.AddToCartView.as_view(),
        name='add-to-cart',
        ),
    path(
        'subtract-from-cart/<int:pk>/',
        views.SubtractFromCartView.as_view(),
        name='subtract-from-cart'
        ),
    path(
        'remove-from-cart/<int:pk>/',
        views.RemoveFromCartView.as_view(),
        name='remove-from-cart'
        ),
]
