from django.views import generic
from django.contrib.auth.views import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.text import slugify

from django.contrib import messages
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .forms import CategoryForm, ItemImageForm, ItemForm
from .models import Category, Item, Shop
from orders.models import ShopOrder


class CheckShopMixin(UserPassesTestMixin):
    # check if staff from this shop
    def test_func(self):
        item = self.get_object()
        return self.request.user.is_staff and \
            self.request.user.userprofile.shop == item.shop


class CheckStaffMixin(UserPassesTestMixin):
    # check if user is staff
    def test_func(self):
        return self.request.user.is_staff


class ShopSettingsView(
        LoginRequiredMixin,
        CheckStaffMixin,
        generic.UpdateView
        ):
    model = Shop
    fields = ['shop_name', 'avatar']
    template_name = 'shop/shop_settings.html'
    success_url = reverse_lazy('shop:shop_admin')

    def get_object(self, queryset=None):
        return self.request.user.shop

    def form_valid(self, form):
        shop_name = form.cleaned_data['shop_name']
        slug = slugify(shop_name)
        if Shop.objects.filter(slug=slug).exclude(pk=self.object.pk).exists():
            messages.error(
                self.request,
                f'Shop with the name "{shop_name}" already exists.'
            )
            return self.form_invalid(form)
        form.instance.slug = slug
        messages.success(self.request, "Shop's settings have been updated")
        return super().form_valid(form)


class ShopAdminView(LoginRequiredMixin, CheckStaffMixin, generic.TemplateView):
    template_name = 'shop/shop_admin_panel.html'


class CategoryListView(LoginRequiredMixin, CheckStaffMixin, generic.ListView):
    model = Category
    template_name = 'shop/category/category_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(
                shop__user=self.request.user
            ).order_by('-id')
        cache_key = 'amount_category'
        amount_category = cache.get(cache_key)
        if amount_category:
            context['amount'] = amount_category
        else:
            amount_category = Category.objects.count()
            context['amount'] = amount_category
            cache.set(cache_key, amount_category)
        return context


class CategoryDetailView(
        LoginRequiredMixin,
        CheckShopMixin,
        generic.DetailView
        ):
    queryset = Category.objects.all()
    template_name = 'shop/category/category_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object
        context['items'] = Item.objects.filter(
                category=category
            ).order_by('-id')
        return context


class CategoryCreateView(
        LoginRequiredMixin,
        CheckStaffMixin,
        generic.CreateView
        ):
    model = Category
    form_class = CategoryForm
    template_name = 'shop/category/category_create_form.html'
    success_url = reverse_lazy('shop:list_category')

    def form_valid(self, form):
        # Set the user and shop on the instance before saving
        shop = self.request.user.shop
        name = form.instance.name

        form.instance.shop = shop
        slug = slugify(name + '-' + str(shop.id))
        # Check if a Category with the same slug already exists
        if Category.objects.filter(slug=slug):
            messages.error(
                self.request,
                f'A category with the name "{slugify(name)}" already exists.'
                )
            return self.form_invalid(form)
        form.instance.slug = slug
        # Call the parent form_valid method to save the instance
        response = super().form_valid(form)
        messages.success(self.request, 'Category created successfully.')
        return response


class CategoryUpdateView(
        LoginRequiredMixin,
        CheckShopMixin,
        generic.UpdateView
        ):
    queryset = Category.objects.all()
    form_class = CategoryForm
    template_name = 'shop/category/category_update_form.html'
    success_url = reverse_lazy('shop:list_category')

    def form_valid(self, form):
        # Set the user and shop on the instance before saving
        shop = self.request.user.shop
        name = form.instance.name

        form.instance.shop = shop
        slug = slugify(name + '-' + str(shop.id))
        # Check if a Category with the same slug already exists
        if Category.objects.filter(slug=slug):
            messages.error(
                self.request,
                f'A category with the name "{slugify(name)}" already exists.'
                )
            return self.form_invalid(form)
        form.instance.slug = slug
        # Call the parent form_valid method to save the instance
        response = super().form_valid(form)
        messages.success(self.request, 'Category created successfully.')
        return response


class CategoryDeleteView(
        LoginRequiredMixin,
        CheckShopMixin,
        generic.DeleteView
        ):
    queryset = Category.objects.all()
    success_url = reverse_lazy('shop:list_category')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Category has been deleted.')
        return response


class ItemListView(
        LoginRequiredMixin,
        CheckStaffMixin,
        generic.ListView
        ):
    model = Item
    template_name = 'shop/item/item_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Item.objects.filter(
            shop__user=self.request.user
        ).order_by('-id')
        return context


class ItemDetailView(
        LoginRequiredMixin,
        CheckShopMixin,
        generic.DetailView
        ):
    queryset = Item.objects.all()
    template_name = 'shop/item/item_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shop"] = self.request.user.shop
        return context


class ItemCreateView(
        LoginRequiredMixin,
        CheckStaffMixin,
        FormView
        ):
    form_class = ItemForm
    image_form_class = ItemImageForm
    template_name = 'shop/item/item_create_form.html'
    success_url = reverse_lazy('shop:list_item')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['shop'] = self.request.user.shop
        return kwargs

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = self.image_form_class()
        context['shop'] = self.request.user.shop
        return context

    def form_valid(self, form):
        image_form = self.image_form_class(
            self.request.POST,
            self.request.FILES
            )
        if image_form.is_valid():
            shop = self.request.user.shop
            name = form.cleaned_data['name']

            item = form.save(commit=False)
            item.shop = shop

            slug = slugify(name + '-' + str(shop.id))
            if Item.objects.filter(slug=slug):
                messages.error(
                    self.request,
                    f'A item with the name "{slugify(name)}" already exists.'
                    )
                return self.form_invalid(form)
            item.slug = slug
            item.save()
            image = image_form.save(commit=False)
            image.image = image_form.cleaned_data['image']

            image.item = item
            image.save()
            return super().form_valid(form)
        else:
            messages.error(self.request, image_form.errors)
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    image_form=image_form
                )
            )

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        messages.error(self.request, form.errors)
        return self.render_to_response(context)


class ItemUpdateView(LoginRequiredMixin, CheckShopMixin, generic.UpdateView):
    model = Item
    form_class = ItemForm
    image_form_class = ItemImageForm
    template_name = 'shop/item/item_update_form.html'
    success_url = reverse_lazy('shop:list_item')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['shop'] = self.request.user.shop
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_image'] = self.get_object().itemimage.last()
        if self.request.POST:
            context['image_form'] = self.image_form_class(
                self.request.POST,
                self.request.FILES
            )
        else:
            context['image_form'] = self.image_form_class()
        context['shop'] = self.request.user.shop
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_form = context['image_form']
        if image_form.is_valid():
            shop = context['shop']
            name = form.cleaned_data['name']

            item = form.save(commit=False)
            item.shop = shop

            slug = slugify(name + '-' + str(shop.id))
            if Item.objects.filter(
                        slug=slug
                    ).exclude(pk=self.object.pk).exists():
                messages.error(
                    self.request,
                    f'A item with the name "{slugify(name)}" already exists.'
                )
                return self.form_invalid(form)
            item.slug = slug
            item.save()
            if image_form.cleaned_data['image'] is not None:
                image = image_form.save(commit=False)
                image.image = image_form.cleaned_data['image']
                image.item = item
                image.save()
            return super().form_valid(form)
        else:
            messages.error(self.request, image_form.errors)
            return self.render_to_response(
                self.get_context_data(
                    form=form, image_form=image_form
                    )
                )


class ItemDeleteView(LoginRequiredMixin, CheckShopMixin, generic.DeleteView):
    queryset = Item.objects.all()
    success_url = reverse_lazy('shop:list_item')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Item has been deleted.')
        return response


class OrdersView(LoginRequiredMixin, CheckStaffMixin, generic.TemplateView):
    template_name = 'shop/orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shop = Shop.objects.get(user=self.request.user)
        shop_orders = ShopOrder.objects.filter(
            shop=shop,
            order__billing_status=True
        )

        context['shop_orders'] = shop_orders
        context['shop'] = shop
        return context


class OrdersDetailView(
        LoginRequiredMixin,
        CheckStaffMixin,
        generic.DetailView
        ):
    template_name = 'shop/details_order.html'
    context_object_name = 'order'

    def get_queryset(self):
        shop = Shop.objects.get(user=self.request.user)
        shop_orders = ShopOrder.objects.filter(
            shop=shop,
            order__billing_status=True
        )
        return shop_orders

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shop = Shop.objects.get(user=self.request.user)
        orderitems = self.get_object().order.items.filter(item__shop=shop)

        context['orderitems'] = orderitems
        return context


class CustomersView(LoginRequiredMixin, CheckStaffMixin, generic.TemplateView):
    template_name = 'shop/customers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shop = Shop.objects.get(user=self.request.user)
        shop_orders = ShopOrder.objects.filter(
            shop=shop,
            order__billing_status=True
        )

        # orders = Order.objects.filter(shops__in=[shop], billing_status=True)
        customers = set()
        for cust in shop_orders:
            customers.add(cust.order.user)

        context['customers'] = customers
        context['shop'] = shop
        return context


class CustomerOrdersViews(
        LoginRequiredMixin,
        CheckStaffMixin,
        generic.TemplateView
        ):
    template_name = 'shop/customer_orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shop = Shop.objects.get(user=self.request.user)
        customer_id = self.kwargs['customer_id']
        customer = get_object_or_404(get_user_model(), id=customer_id)

        shop_orders = ShopOrder.objects.filter(
            shop=shop,
            order__billing_status=True,
            order__user=customer
        )

        context['customer'] = customer
        context['shop_orders'] = shop_orders
        return context
