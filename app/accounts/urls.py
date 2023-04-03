from django.urls import path
from . import views

app_name = 'accounts'


urlpatterns = [
    path('login/', views.SignInView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),

    path(
        'activate/<uidb64>/<token>/',
        views.ActivationView.as_view(),
        name='activate'
      ),
]
