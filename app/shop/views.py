from django.views import generic, View
from django.contrib.auth.views import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.shortcuts import redirect


from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.core.paginator import Paginator

from .forms import (
    CategoryForm,
    ShopStatusForm,
    ItemImageForm,
    ItemForm,
    OrderStatusForm,
    ItemStatusForm
)
from .models import Category, Item, Shop
from orders.models import ShopOrder


class CheckSuperMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


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
    fields = ['shop_name', 'avatar', 'cover_photo']
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


class ShopAdminView(
        LoginRequiredMixin,
        CheckStaffMixin,
        generic.TemplateView
        ):
    template_name = 'shop/shop_admin_panel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shop = Shop.objects.get(user=self.request.user)
        orders = ShopOrder.objects.filter(
            shop=shop,
            order__billing_status=True
        )
        # list of ordered items for shop
        # like this [<QuerySet [<OrderItem: Happy place-Book Land-3TjHeyX>,]
        list_orderitems = [
            order.order.items.filter(item__shop=shop) for order in orders
            ]
        # dct store item: amount sold
        # {<Item: Happy place>: 3, <Item: Atlas shrugged>: 4,}
        dct = {}
        for qs in list_orderitems:
            for item in qs:
                if item.item in dct:
                    dct[item.item] += item.quantity
                else:
                    dct[item.item] = item.quantity

        context["total_revenue"] = sum([order.price for order in orders])
        context["item_amount"] = dct.items()
        context["orders"] = orders
        return context


class CategoryListView(
        LoginRequiredMixin,
        CheckStaffMixin,
        generic.ListView
        ):
    template_name = 'shop/category/category_list.html'
    paginate_by = 10
    context_object_name = 'categories'

    def get_queryset(self):
        queryset = Category.objects.filter(
                shop__user=self.request.user
            ).order_by('-id')

        return queryset


class CategoryDetailView(
        LoginRequiredMixin,
        CheckShopMixin,
        generic.DetailView
        ):
    queryset = Category.objects.all()
    template_name = 'shop/category/category_details.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object
        items = Item.objects.filter(category=category).order_by('-id')

        paginator = Paginator(items, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['items'] = page_obj
        context['is_paginated'] = page_obj.has_other_pages()
        context['page_obj'] = page_obj
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
    context_object_name = 'items'
    paginate_by = 10

    def get_queryset(self):
        queryset = Item.objects.filter(
            shop__user=self.request.user
        ).order_by('-id')

        return queryset


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


class ItemUpdateView(
        LoginRequiredMixin,
        CheckShopMixin,
        generic.UpdateView
        ):
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


class ItemDeleteView(
        LoginRequiredMixin,
        CheckShopMixin,
        generic.DeleteView
        ):
    queryset = Item.objects.all()
    success_url = reverse_lazy('shop:list_item')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Item has been deleted.')
        return response


class OrdersView(
        LoginRequiredMixin,
        CheckStaffMixin,
        generic.ListView
        ):
    template_name = 'shop/orders.html'
    context_object_name = 'shop_orders'
    paginate_by = 10

    def get_queryset(self):
        shop = Shop.objects.get(user=self.request.user)
        queryset = ShopOrder.objects.filter(
            shop=shop,
            order__billing_status=True
        )

        return queryset


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
        context['form'] = OrderStatusForm(instance=self.get_object())
        return context


class UpdateOrderStatusView(View):
    def post(self, request, *args, **kwargs):
        order_pk = self.kwargs['pk']
        form = OrderStatusForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data['status']
            order = ShopOrder.objects.get(pk=order_pk)
            order.status = status
            order.save()
            messages.success(request, 'Order status updated successfully.')
        else:
            messages.error(request, 'Invalid form data. Please try again.')
        return redirect('shop:orders')


class CustomersView(
        LoginRequiredMixin,
        CheckStaffMixin,
        generic.ListView
        ):
    template_name = 'shop/customers.html'
    paginate_by = 10
    context_object_name = 'customers'

    def get_queryset(self):
        shop = Shop.objects.get(user=self.request.user)
        shop_orders = ShopOrder.objects.filter(
            shop=shop,
            order__billing_status=True
        )
        queryset = set()
        for cust in shop_orders:
            queryset.add(cust.order.user)

        return list(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shop = Shop.objects.get(user=self.request.user)
        context['shop'] = shop
        return context


class CustomerOrdersViews(
        LoginRequiredMixin,
        CheckStaffMixin,
        generic.ListView
        ):
    template_name = 'shop/customer_orders.html'
    paginate_by = 10
    context_object_name = 'shop_orders'

    def get_queryset(self):
        shop = Shop.objects.get(user=self.request.user)
        customer_id = self.kwargs['customer_id']
        customer = get_object_or_404(get_user_model(), id=customer_id)
        queryset = ShopOrder.objects.filter(
            shop=shop,
            order__billing_status=True,
            order__user=customer
        )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer_id = self.kwargs['customer_id']
        customer = get_object_or_404(get_user_model(), id=customer_id)
        context['customer'] = customer
        return context


class SuperUserPanelShops(
        LoginRequiredMixin,
        CheckSuperMixin,
        generic.ListView
        ):

    template_name = 'shop/superuser/new_shops.html'
    model = Shop
    context_object_name = 'shops'
    paginate_by = 10
    ordering = ['-created_at', ]


class SuperUserPanelItems(
        LoginRequiredMixin,
        CheckSuperMixin,
        generic.ListView
        ):
    template_name = 'shop/superuser/new_items.html'
    model = Item
    context_object_name = 'items'
    paginate_by = 10
    ordering = ['-created_at', ]


class ShopDetailAdminView(
        LoginRequiredMixin,
        CheckSuperMixin,
        generic.DetailView,
        ):
    template_name = 'shop/superuser/new_shop_details.html'
    model = Shop
    context_object_name = 'shop'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'download-docs' in request.GET:
            return self.download_docs()
        else:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ShopStatusForm(instance=self.object)
        return context

    def download_docs(self):
        shop = self.get_object()
        file_contents = shop.docs.read()
        response = HttpResponse(
            file_contents,
            content_type='application/octet-stream'
        )
        file_name = f'attachment; filename="{shop.shop_name}"'
        response['Content-Disposition'] = file_name
        return response


class ItemDetailAdminView(
        LoginRequiredMixin,
        CheckSuperMixin,
        generic.DetailView,
        ):
    template_name = 'shop/superuser/new_item_details.html'
    model = Item
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ItemStatusForm(instance=self.object)
        return context


class ShopApprovedView(
        LoginRequiredMixin,
        CheckSuperMixin,
        View,
        ):

    def post(self, request, *args, **kwargs):
        shop_slug = self.kwargs['slug']
        form = ShopStatusForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data['is_approved']
            shop = Shop.objects.get(slug=shop_slug)
            shop.is_approved = status
            shop.save()
            messages.success(request, 'Shop status updated successfully.')
        else:
            messages.error(request, 'Invalid form data. Please try again.')
        return redirect('shop:super_user_panel_shops')


class ItemApprovedView(
        LoginRequiredMixin,
        CheckSuperMixin,
        View,
        ):

    def post(self, request, *args, **kwargs):
        item_slug = self.kwargs['slug']
        form = ItemStatusForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data['is_approved']
            item = Item.objects.get(slug=item_slug)
            item.is_approved = status
            item.save()
            messages.success(request, 'Item status updated successfully.')
        else:
            messages.error(request, 'Invalid form data. Please try again.')
        return redirect('shop:super_user_panel_shops_items')
