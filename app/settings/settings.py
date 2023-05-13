import os
from pathlib import Path
from decouple import config
from django.contrib.messages import constants as messages
from celery.schedules import crontab

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['*']

# LOGIN_REDIRECT_URL = 'marketplace:home_view'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # additional django
    'django_extensions',
    'django_celery_beat',
    'debug_toolbar',
    'cities_light',
    'ajax_select',
    'widget_tweaks',

    # apps
    'accounts',
    'marketplace',
    'shop',
    'cart',
    'payment',
    'orders',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # debug
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]

ROOT_URLCONF = 'settings.urls'

# enable caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# set the cache timeout to 5 minutes
CACHE_TTL = 300

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(BASE_DIR.parent, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'accounts.context_processors.daily_newsletter_form',
                'accounts.context_processors.get_google_api',
                'cart.context_processors.cart_counter',
            ],
        },
    },
]

WSGI_APPLICATION = 'settings.wsgi.application'

# postgresql db
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

#debug config
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.history.HistoryPanel',
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]
INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]
# email config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    messages.WARNING: 'warning',
    messages.SUCCESS: 'success',
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR /'assets'
STATICFILES_DIRS = [BASE_DIR / "static"]

# media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR.parent / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = "accounts.User"

# email config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

CELERY_BROKER_URL = 'amqp://localhost'
CELERY_TIMEZONE = 'Europe/Warsaw'
CELERY_BEAT_SCHEDULE = {
    'send_daily_newsletter': {
        'task': 'accounts.tasks.send_daily_newsletter',
        'schedule': crontab(hour=10, minute=0),  # runs every day at 8am
    },
}

# location
GOOGLE_API_KEY = config('GOOGLE_API_KEY')

STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')

STRIPE_ENDPOINT_SECRET = config('STRIPE_ENDPOINT_SECRET')
