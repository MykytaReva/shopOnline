from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.contrib.auth.views import PasswordChangeView

from accounts.models import UserProfile
from shop.models import Item
from orders.models import Order
from .forms import UserForm, UserProfileForm


class CheckShopMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_staff


class CustomerPanelView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'customers/customer_panel.html'


class CustomerProfileView(LoginRequiredMixin, generic.UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    user_form_class = UserForm
    template_name = 'customers/customer_profile.html'
    success_url = reverse_lazy('customers:customer_panel')

    def get_object(self, queryset=None):
        return self.request.user.userprofile

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
        return render(
            self.request,
            self.template_name,
            context=context
        )


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    model = get_user_model()
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('customers:customer_panel')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Password has been changed!')

        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        messages.error(
            self.request,
            form.errors
        )

        return render(
            self.request,
            self.template_name,
            context=context
        )


class WishListView(LoginRequiredMixin, generic.ListView):
    model = Item
    template_name = 'customers/wish_list.html'
    context_object_name = 'items'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wish_list'] = self.request.user.wish_list.all()
        context['wish_count'] = self.request.user.wish_list.count()
        return context


class OrdersView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'customers/orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(user=self.request.user)
        return context


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'customers/details_order.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['orderitems'] = self.get_object().items.all()
        context['total'] = self.get_object().total_paid
        return context
