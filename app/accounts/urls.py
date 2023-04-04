from django.urls import path
from . import views
from .context_processors import daily_newsletter_form
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
    path('newsletter/', daily_newsletter_form, name='newsletter'),

]
