from django.db import models
from accounts.models import User, UserProfile


def shop_docs(instance, filename):
    return 'docs/{0}/{1}'.format(instance.user.id, filename)


def shop_avatar(instance, filename):
    return 'shopAvatar/{0}/{1}'.format(instance.user.id, filename)


def shop_cover(instance, filename):
    return 'shopCover/{0}/{1}'.format(instance.user.id, filename)


def item_photo(instance, filename):
    return 'item_photo/{0}/{1}'.format(instance.item.id, filename)


class Shop(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='shop'
    )
    user_profile = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='shop'
    )
    shop_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    docs = models.FileField(upload_to=shop_docs)
    avatar = models.ImageField(
        upload_to=shop_avatar,
        blank=True,
        null=True
        )
    cover_photo = models.ImageField(
        upload_to=shop_cover,
        blank=True,
        null=True
        )
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.shop_name


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name='categories',
        null=True
        )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def clean(self):
        self.name = self.name.capitalize()

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=55)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='items',
        null=True
        )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name='items',
        null=True,
        )
    slug = models.SlugField(unique=True)
    # wish list
    wish_list = models.ManyToManyField(
        User,
        related_name='wish_list',
        blank=True
        )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_approved = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def clean(self):
        self.name = self.name.capitalize()
        self.title = self.title.capitalize()


class ItemImage(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='itemimage',
        null=True
    )
    image = models.ImageField(upload_to=item_photo)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name} - {self.item.id}"

    class Meta:
        get_latest_by = 'created_at'
