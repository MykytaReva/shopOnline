from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.contrib import messages
from django.contrib.auth import get_user_model

from accounts.models import UserProfile

from .forms import UserForm, UserProfileForm

from django.core.cache import cache
from django.contrib.auth.views import PasswordChangeView


class CustomerPanelView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'customers/customer_panel.html'


class CustomerProfileView(LoginRequiredMixin, generic.UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    user_form_class = UserForm
    template_name = 'customers/customer_profile.html'
    success_url = reverse_lazy('customers:customer_panel')

    def get_object(self, queryset=None):
        # check if the user profile is already in cache
        user_profile = cache.get('user_profile_{}'.format(
            self.request.user.userprofile.pk
            ))
        if user_profile is None:
            # if not, retrieve it from the database and store it in the cache
            user_profile = super().get_object(
                queryset
                )
            cache.set('user_profile_{}'.format(
                self.request.user.userprofile.pk
                ), user_profile)
        return user_profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['user_form'] = self.user_form_class(
                self.request.POST,
                instance=self.request.user,
            )
        else:
            context['user_form'] = self.user_form_class(
                instance=self.request.user
                )
            context['form'] = self.form_class(
                instance=self.request.user.userprofile
                )
            context['profile'] = self.request.user.userprofile
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']

        if user_form.is_valid():
            user_form.save()
            return super().form_valid(form)
        else:
            messages.error(self.request, user_form.errors)
            return self.render(
                self.request,
                self.template_name,
                context={'form': form, 'user_form': user_form}
            )

        cache.delete('user_profile_{}'.format(
            self.request.user.userprofile.pk
            ))
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        messages.error(self.request, form.errors)
        return self.render(
            self.request,
            self.template_name,
            context=context
        )


class ChangePasswordView(PasswordChangeView):
    model = get_user_model()
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('customers:customer_panel')

    def form_valid(self, form):
        messages.success(self.request, 'Password has been changed!')

        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        messages.error(
            self.request,
            form.errors
        )
        print(form.errors)
        return render(
            self.request,
            self.template_name,
            context=context
        )
