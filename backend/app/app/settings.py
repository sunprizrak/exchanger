from pathlib import Path
from .config import settings
from celery.schedules import crontab

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = settings.django.secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = settings.django.debug

ALLOWED_HOSTS = settings.django.allowed_hosts


# Application definition

INSTALLED_APPS = [
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'orders',
    'coins',
    'payment_methods',
    'graphene_django',
    'django_celery_beat',
    'corsheaders',
    'django_cleanup.apps.CleanupConfig',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": settings.db.engine,
        "NAME": settings.db.name,
        "USER": settings.db.user,
        "PASSWORD": settings.db.password,
        "HOST": settings.db.host,
        "PORT": settings.db.port,
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = settings.django.language_code

TIME_ZONE = settings.django.time_zone

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

SITE_URL = settings.django.site_url

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = (
    'graphql_jwt.backends.JSONWebTokenBackend',
    'users.backends.CustomAuthBackend',
)

GRAPHENE = {
    "SCHEMA": "app.schema.schema",
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = ("http://127.0.0.1:5173", "https://rnpka-37-214-64-61.a.free.pinggy.link",)

TELEGRAM_BOT_TOKEN = settings.tg.telegram_bot_token

CELERY_BROKER_URL = settings.celery.broker_url
CELERY_RESULT_BACKEND = settings.celery.result_backend
CELERY_ACCEPT_CONTENT = settings.celery.accept_content
CELERY_TASK_SERIALIZER = settings.celery.task_serializer
CELERY_RESULT_SERIALIZER = settings.celery.result_serializer

CELERY_BEAT_SCHEDULE = {
    'update-currencies-and_coins-price': {
        'task': 'coins.tasks.update_currencies_and_coins_price',
        'schedule': 300.0,  # 300 секунд = 5 минут
    },
}