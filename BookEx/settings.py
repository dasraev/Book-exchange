
from pathlib import Path
import os
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
}
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5gotzi*)$b_rc7$j5z^5gzh__rgc&x-0g_v1i3*z!w(#5__(@e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','0.0.0.0','localhost','.pythonanywhere.com','bookexchange.pythonanywhere.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'crispy_forms',
    "django.contrib.postgres",  # new
    'book',
    'user',
    'api',
    "debug_toolbar",
    'rest_framework',
    'rest_framework.authtoken',
    'celery',
    'chat',
    'channels',

]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'BookEx.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'BookEx.wsgi.application'
ASGI_APPLICATION = 'BookEx.asgi.application'



# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'book',
#         'USER': 'postgres',
#         'PASSWORD': 'postgres',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'book',
#         'USER': 'super',
#         'PASSWORD': 'dasraev05092000',
#         'HOST': 'bookexchange-3212.postgres.pythonanywhere-services.com',
#         'PORT': '13212',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

STATIC_URL = 'static/'
# STATIC_ROOT = BASE_DIR /'static'
STATICFILES_DIRS = [BASE_DIR /'static']

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'user.MyUser'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'
LOGIN_URL = 'login'
#
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PORT = 25
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'testdasraev@gmail.com'
EMAIL_HOST_PASSWORD = 'vjwsgwuwzqimkysi'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}



SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}






# Celery settings
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# myproject/settings.py

# Celery Configuration Options
CELERY_TIMEZONE = 'UTC'

# Celery Beat Configuration Options
# myproject/settings.py
from celery.schedules import crontab

# Celery Beat Configuration Options
CELERY_BEAT_SCHEDULE = {
    'get_users_daily': {
        'task': 'api.tasks.get_users',  # Path to your Celery task
        'schedule': crontab(hour=10-5, minute=30),  # Run the task every day at 8 am
    },
}

