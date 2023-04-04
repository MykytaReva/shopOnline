from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages, auth
from django.template.defaultfilters import slugify

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import View

from django.contrib.auth import get_user_model

from .forms import SignUpForm
from .tasks import send_activation_email


from shop.models import Shop
from shop.forms import ShopForm


class SignInView(LoginView):
    success_url = reverse_lazy('marketplace:home_view')
    template_name = 'accounts/login.html'

    def form_valid(self, email, password):
        """Security check complete. Log the user in."""
        if get_user_model().objects.filter(email=email).exists():
            user = auth.authenticate(email=email, password=password)
            return user

    def post(self, request, *args, **kwargs):
        super().post(self.request, *args, **kwargs)
        email = self.request.POST['email']
        password = self.request.POST['password']
        user = self.form_valid(email, password)
        print(user)
        # check if account exists:
        if not get_user_model().objects.filter(email=email).exists():
            messages.error(
                self.request,
                'Acount with this email address does not exists.'
            )
            return redirect('accounts:login')
        if user is not None:
            if user.is_active:
                auth.login(self.request, user)
                messages.success(self.request, 'You are logged in!)')
                return redirect('marketplace:home_view')
            else:
                messages.error(
                    self.request,
                    'Activate your account by email first'
                )
                return redirect('accounts:login')
        else:
            messages.error(self.request, 'Incorrect password.')
            return redirect('accounts:login')
        return redirect('accounts:login')


class LogoutView(LogoutView):
    template_name = reverse_lazy('marketplace:home_view')

    def get(self, request):
        # check if user logged in
        if not request.user.is_authenticated:
            messages.error(request, 'You are already logged out!')
            return redirect('marketplace:home_view')

        auth.logout(request)
        messages.success(request, 'You are logged out')

        return redirect(reverse_lazy('marketplace:home_view'))


class SignUpView(View):

    def get(self, request, *args, **kwargs):
        u_form = SignUpForm()
        s_form = ShopForm()
        context = {
            'u_form': u_form,
            's_form': s_form
        }

        return render(self.request, 'accounts/signup.html', context)

    def post(self, request, *args, **kwargs):
        u_form = SignUpForm(self.request.POST)
        s_form = ShopForm(self.request.POST, self.request.FILES)
        if u_form.is_valid():
            # get credentials for user
            first_name = u_form.cleaned_data['first_name']
            last_name = u_form.cleaned_data['last_name']
            username = u_form.cleaned_data['username']
            email = u_form.cleaned_data['email']
            password = u_form.cleaned_data['password1']
            # Role
            role = self.request.POST['inlineRadioOptions']
            u_form.cleaned_data['role'] = role

            # check if user or shop
            if role == 'thisuser':
                # create user
                user = get_user_model().objects.create_user(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    password=password,
                    role=1
                )
            elif role == 'thisshop':
                if s_form.is_valid():
                    # get credentials for Shop
                    shop_name = s_form.cleaned_data['shop_name']
                    docs = s_form.cleaned_data['docs']
                    slug = slugify(shop_name)

                    user = get_user_model().objects.create_user(
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        username=username,
                        password=password,
                        role=2,
                    )

                    shop = Shop.objects.create(
                        user=user,
                        user_profile=user.userprofile,
                        shop_name=shop_name,
                        docs=docs,
                        slug=slug
                    )
                else:
                    # messages.error(self.request, s_form.errors)
                    messages.error(self.request, u_form.errors)
                    u_form = SignUpForm()
                    s_form = ShopForm()

            messages.success(
                self.request,
                'Account created, check your inbox for the activation email.'
            )
            # send email through celery passing userPk
            send_activation_email.delay(user.pk)
            return redirect('accounts:login')
        else:
            messages.error(self.request, u_form.errors)
            messages.error(self.request, s_form.errors)

            u_form = SignUpForm()
            s_form = ShopForm()
        context = {
            'u_form': u_form,
            's_form': s_form,
        }
        return render(self.request, 'accounts/signup.html', context)


class ActivationView(View):
    def get(self, request, uidb64, token):
        # Activate the user by setting the is_active to the True
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            get_user_model().DoesNotExist
        ):
            user = None

        if user is not None \
                and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(
                request,
                'Congratulations! Your account is activated.'
            )
            return redirect('marketplace:home_view')
        else:
            messages.error(request, 'Invalid activation link.')
            return redirect('marketplace:home_view')

        return redirect('accounts:login')
