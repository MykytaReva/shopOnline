from django.urls import path
from .views import HomeView


app_name = 'marketplace'

urlpatterns = [
    path('', HomeView.as_view(), name='home_view'),
]
