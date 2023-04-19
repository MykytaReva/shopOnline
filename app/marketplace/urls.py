from django.urls import path
from . import views


app_name = 'marketplace'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home_view'),
    path(
        'add-wish/<int:id>/',
        views.AddToWishListView.as_view(),
        name='add_wish'
        ),
    path(
        'item-details/<slug:slug>',
        views.ItemFullView.as_view(),
        name='item_details'
        ),
    path(
        'shop/<slug:slug>/items/',
        views.ShopView.as_view(),
        name='shop'
        ),
    path(
        'shop/<slug:slug>/items/<slug:category_slug>/',
        views.ShopView.as_view(),
        name='shop_by_category'
    ),

]
