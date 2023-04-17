from django.views import generic
from django.contrib.auth.views import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.text import slugify

from django.contrib import messages
from django.core.cache import cache

from .forms import CategoryForm, ItemImageForm, ItemForm
from .models import Category, Item


class ShopAdminView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'shop/shop_admin_panel.html'


class CategoryListView(LoginRequiredMixin, generic.ListView):
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


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    queryset = Category.objects.all()
    template_name = 'shop/category/category_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object
        context['items'] = Item.objects.filter(
                category=category
            ).order_by('-id')
        return context


class CategoryCreateView(LoginRequiredMixin, generic.CreateView):
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


class CategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
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


class CategoryDeleteView(LoginRequiredMixin, generic.DeleteView):
    queryset = Category.objects.all()
    success_url = reverse_lazy('shop:list_category')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Category has been deleted.')
        return response


class ItemListView(LoginRequiredMixin, generic.ListView):
    model = Item
    template_name = 'shop/item/item_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Item.objects.filter(
            shop__user=self.request.user
        ).order_by('-id')
        return context


class ItemDetailView(LoginRequiredMixin, generic.DetailView):
    queryset = Item.objects.all()
    template_name = 'shop/item/item_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shop"] = self.request.user.shop
        return context


class ItemCreateView(LoginRequiredMixin, FormView):
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


class ItemUpdateView(LoginRequiredMixin, generic.UpdateView):
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

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        messages.error(self.request, form.errors)
        return self.render_to_response(context)


class ItemDeleteView(LoginRequiredMixin, generic.DeleteView):
    queryset = Item.objects.all()
    success_url = reverse_lazy('shop:list_item')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Item has been deleted.')
        return response
