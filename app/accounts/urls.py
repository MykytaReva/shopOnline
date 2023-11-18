from django.urls import path

from . import views
from .context_processors import daily_newsletter_form

app_name = "accounts"


urlpatterns = [
    path("login/", views.SignInView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("activate/<uidb64>/<token>/", views.ActivationView.as_view(), name="activate"),
    path("newsletter/", daily_newsletter_form, name="newsletter"),
    # reset password
    path("forgot_password/", views.ForgotPasswordView.as_view(), name="forgot_password"),
    path(
        "reset_password_validate/<uidb64>/<token>/",
        views.ValidatePasswordView.as_view(),
        name="validate_password",
    ),
    path("reset_password/", views.ResetPasswordView.as_view(), name="reset_password"),
]
