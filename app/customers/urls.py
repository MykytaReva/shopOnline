from django.urls import path
from . import views

app_name = 'customers'


urlpatterns = [
    path('', views.CustomerPanelView.as_view(), name='customer_panel'),
    path(
        'profile-settings/',
        views.CustomerProfileView.as_view(),
        name='profile_settings'
        ),

    path(
        'change-password/',
        views.ChangePasswordView.as_view(),
        name='change_password'
        ),
    path('wish-list/', views.WishListView.as_view(), name='wish_list'),
]
