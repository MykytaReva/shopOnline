import logging
import os
from pathlib import Path

import sentry_sdk
from celery.schedules import crontab
from decouple import config
from django.contrib.messages import constants as messages

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = config("SECRET_KEY")


ALLOWED_HOSTS = ["nsrevas.bio", "138.68.82.89"]

ADMIN_ENABLED = False
ENV = config("ENV")
if ENV == "dev":
    ADMIN_ENABLED = True
    DEBUG = True
    ALLOWED_HOSTS = ["nsrevas.bio", "*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # additional django
    "django_extensions",
    "django_celery_beat",
    "cities_light",
    "ajax_select",
    "widget_tweaks",
    # apps
    "accounts",
    "marketplace",
    "shop",
    "cart",
    "payment",
    "orders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "settings.urls"

# enable caching
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": "127.0.0.1:11211",
    }
}

# set the cache timeout to 5 minutes
CACHE_TTL = 300

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "accounts.context_processors.daily_newsletter_form",
                "accounts.context_processors.get_google_api",
                "cart.context_processors.cart_counter",
                "shop.context_processors.get_new_orders_count",
                "shop.context_processors.get_not_approved_numbers",
            ],
        },
    },
]

WSGI_APPLICATION = "settings.wsgi.application"

# postgresql db
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("POSTGRES_HOST"),
        "PORT": config("POSTGRES_PORT"),
    }
}

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]
MESSAGE_TAGS = {
    messages.ERROR: "danger",
    messages.WARNING: "warning",
    messages.SUCCESS: "success",
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# static files
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
# STATICFILES_DIRS = (os.path.join(BASE_DIR, "static/"),)


# media files
MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom User Model
AUTH_USER_MODEL = "accounts.User"

# location
GOOGLE_API_KEY = config("GOOGLE_API_KEY")

STRIPE_PUBLISHABLE_KEY = config("STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY")

STRIPE_ENDPOINT_SECRET = config("STRIPE_ENDPOINT_SECRET")

if ENV != "dev":
    sentry_sdk.init(
        dsn=config("SENTRY_DSN"),
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

SENDGRID_API_KEY = config("SENDGRID_API_KEY")
FROM_EMAIL = config("FROM_EMAIL")


# Celery Configuration
CELERY_BROKER_URL = config("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"

CELERY_BEAT_SCHEDULE = {
    "send_daily_newsletter": {
        "task": "accounts.tasks.send_daily_newsletter",
        "schedule": crontab(hour=10, minute=0),  # runs every day at 8am
    },
}
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
