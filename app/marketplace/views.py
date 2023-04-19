from django.views import generic
from shop.models import Item, Shop, Category
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages


class HomeView(generic.ListView):
    model = Item
    template_name = 'marketplace/home.html'
    context_object_name = 'items'
    paginate_by = 8

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ShopView(generic.ListView):
    template_name = 'marketplace/shop_page.html'
    context_object_name = 'items'
    paginate_by = 8

    def get_queryset(self):
        shop = Shop.objects.get(slug=self.kwargs['slug'])
        category_slug = self.kwargs.get('category_slug')
        items = Item.objects.filter(shop=shop)
        if category_slug:
            category = Category.objects.filter(
                shop=shop, slug=category_slug
                ).first()
            if category:
                items = items.filter(category=category)
        return items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop'] = Shop.objects.get(slug=self.kwargs['slug'])
        context['categories'] = Category.objects.filter(shop=context['shop'])
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            shop = Shop.objects.get(slug=self.kwargs['slug'])
            context['current_category'] = 'Category: {}'.format(
                Category.objects.filter(shop=shop, slug=category_slug).first()
                )
        else:
            context['current_category'] = 'All Products'
        context['selected_category'] = self.kwargs.get('category_slug')
        return context


class AddToWishListView(LoginRequiredMixin, View):
    login_required_message = "Please log in to add product to Wish List"

    def post(self, request, id):
        item = get_object_or_404(Item, id=id)
        if item.wish_list.filter(id=self.request.user.id).exists():
            item.wish_list.remove(self.request.user)
            messages.warning(
                self.request,
                '"{}" has been removed from WishList.'.format(item.name)
            )
        else:
            item.wish_list.add(self.request.user)
            messages.success(
                self.request,
                '{} has been added to WishList'.format(item.name)
            )
        return redirect(request.META["HTTP_REFERER"])

    def dispatch(self, request, *args, **kwargs):
        # redirect if request method Get
        if self.request.method == 'GET':
            return redirect('marketplace:home_view')
        # show reason of login
        elif not self.request.user.is_authenticated:
            messages.warning(self.request, self.login_required_message)
        return super().dispatch(request, *args, **kwargs)


class ItemFullView(generic.DetailView):
    queryset = Item.objects.all()
    template_name = 'marketplace/item_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
