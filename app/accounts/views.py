from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages, auth
from django.views.generic import View, CreateView
from django.http import HttpResponseRedirect, HttpResponse
from django.template.defaultfilters import slugify

from .models import User
from .forms import SignUpForm

from shop.models import Shop
# from shop.forms import ShopForm


class SignInView(View):
    # Login View
    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        # check if user already logged in or not
        if request.user.is_authenticated:
            messages.error(request, 'You are already logged in!')
            return redirect('marketplace:home_view')
        # get credentials for login
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                messages.success(request, 'You are logged in.')
                return HttpResponseRedirect(
                    reverse_lazy('marketplace:home_view')
                )
            else:
                messages.error(request, 'You are logged in.')
                return HttpResponse("Inactive user.")

        else:
            return HttpResponseRedirect(reverse_lazy('marketplace:home_view'))

        return render(request, 'accounts/login.html')


class LogoutView(View):
    # Logour View
    def get(self, request):
        # check if user logged in
        if not request.user.is_authenticated:
            messages.error(request, 'You are already logged out!')
            return redirect('marketplace:home_view')

        auth.logout(request)
        messages.success(request, 'You are logged out')

        return HttpResponseRedirect(reverse_lazy('marketplace:home_view'))


class SignUpView(CreateView):
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')
    success_message = "Your profile was created successfully"

    def post(self, *args, **kwargs):
        form = SignUpForm(self.request.POST)
        # s_form = ShopForm(self.request.POST, request.FILES)
        if form.is_valid():
            # get credentials for user
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            # Role
            role = self.request.POST['inlineRadioOptions']
            print(self.request.POST)
            # check if user or shop
            if role == 'thisuser':
                # create user

                user = User.objects.create_user(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    password=password,
                    role=1
                )
            elif role == 'thisshop':
                # get credentials for Shop
                shop_name = self.request.POST['shop_name']
                docs = self.request.POST['docs']
                slug = slugify(shop_name)

                user = User.objects.create_user(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    password=password,
                    role=2,
                )
                print(user.user_profile)
                shop = Shop.objects.create(
                    user=user,
                    user_profile=user.user_profile,
                    docs=docs,
                    slug=slug
                )

            # send activation email
            # mail_subject = 'Please activate your account.'
            # email_template =
            # 'accounts/emails/account_verification_email.html'
            # send_verification_email(
            # request, user, mail_subject, email_template
            # )
            messages.success(
                self.request,
                'Account created, check your inbox for the activation email.'
            )

            return redirect('accounts:login')
        else:
            messages.error(self.request, form.errors)
            form = SignUpForm()

            return redirect('accounts:signup')
