from django.urls import path
from . import views

app_name = 'customers'


urlpatterns = [
    path('', views.CustomerPanelView.as_view(), name='customer_panel'),
    path(
        'profile-settings/<int:pk>/',
        views.CustomerProfileView.as_view(),
        name='profile_settings'
        ),
]
