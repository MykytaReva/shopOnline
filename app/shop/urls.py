from django.urls import path
from . import views


app_name = 'shop'

urlpatterns = [
    path('', views.ShopAdminView.as_view(), name='shop_admin'),

    # CRUD category
    path(
        'list-category/',
        views.CategoryListView.as_view(),
        name='list_category'
        ),
    path(
        'create-category/',
        views.CategoryCreateView.as_view(),
        name='create_category'
        ),
    path(
        'update-category/<slug:slug>',
        views.CategoryUpdateView.as_view(),
        name='update_category'
        ),
    path(
        'delete-category/<slug:slug>',
        views.CategoryDeleteView.as_view(),
        name='delete_category'
        ),
    path(
        'detail-category/<slug:slug>',
        views.CategoryDetailView.as_view(),
        name='detail_category'
    ),

    # CRUD item
    path(
        'list-item/',
        views.ItemListView.as_view(),
        name='list_item'
        ),
    path(
        'create-item/',
        views.ItemCreateView.as_view(),
        name='create_item'
        ),
    path(
        'update-item/<slug:slug>',
        views.ItemUpdateView.as_view(),
        name='update_item'
        ),
    path(
        'delete-item/<slug:slug>',
        views.ItemDeleteView.as_view(),
        name='delete_item'
        ),
    path(
        'detail-catitemegory/<slug:slug>',
        views.ItemDetailView.as_view(),
        name='detail_item'
        ),

]
