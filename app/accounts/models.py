from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth import get_user_model


# Separate folder for each user
def user_avatar(instance, filename):
    return 'avatar/{0}/{1}'.format(instance.user.id, filename)


class UserManager(BaseUserManager):
    # Custom User Manager
    def create_user(
        self, first_name, last_name, username, email, role=None, password=None
                    ):
        if not email:
            raise ValueError('User must have an email address.')
        if not username:
            raise ValueError('User must have an username.')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            role=role
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, first_name, last_name, username, email, password=None
                        ):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    # Shop or customer account
    SHOP = 2
    CUSTOMER = 1

    ROLE_CHOICE = (
        (SHOP, 'Shop'),
        (CUSTOMER, 'Customer'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICE,
        blank=True,
        null=True
    )

    # Required fields
    created_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    # User permissions
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        blank=True
        )
    profile_picture = models.ImageField(
        upload_to=user_avatar,
        blank=True,
        null=True
        )
    phone_number = models.CharField(max_length=14, blank=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=16, blank=True, null=True)
    city = models.CharField(max_length=16, blank=True, null=True)
    state = models.CharField(max_length=40, blank=True, null=True)
    pin_code = models.CharField(max_length=15, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class DailyLetter(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email.split("@")[0]
