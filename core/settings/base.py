"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.2.17.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
import sys
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR / 'apps'))

from core.configs import get_configs
from kafka import KafkaTopic
from kafka import utils as kafka_utils
from .logger import *

configs = get_configs()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = configs.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "rest_framework",
    "drf_spectacular",
    'corsheaders',
    "debug_toolbar",
    'rest_framework_simplejwt.token_blacklist',

    'user',
    'quiz',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

# Allow specific headers (if needed)
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
CORS_ALLOW_CREDENTIALS = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'
INTERNAL_IPS = [
    '127.0.0.1',
    # Add other IPs if necessary
]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = configs.get_databases()

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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
AUTH_USER_MODEL = 'user.User'
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'login': '2/day'
    },
    'EXCEPTION_HANDLER': 'api.handlers.custom_exception_handler',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Slasify API',
    'DESCRIPTION': 'V1 of the Slasify API',
    'VERSION': '1.0.0',
    # Other settings
}

TEST_DISCOVERY_PATTERN = 'tests.py'


# JWT settings for Simple JWT
SIMPLE_JWT = {
    # The lifetime of the access token. Default is 5 minutes.
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),  # Increase access token lifetime to 1 hour

    # The lifetime of the refresh token. Default is 1 day.
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),  # Increase refresh token lifetime to 7 days

    # Whether to rotate refresh tokens on each use. Default is False.
    'ROTATE_REFRESH_TOKENS': False,

    # Whether to blacklist the old refresh token when it is rotated. Default is False.
    'BLACKLIST_AFTER_ROTATION': False,

    # The algorithm used to sign the token. Default is 'HS256'.
    'ALGORITHM': 'HS256',

    # The signing key used to sign the token. Default is settings.SECRET_KEY.
    'SIGNING_KEY': 'settings.SECRET_KEY',

    # The verification key used to verify the token. Default is None.
    'VERIFYING_KEY': None,

    # The audience claim for the token. Default is None.
    'AUDIENCE': None,

    # The issuer claim for the token. Default is None.
    'ISSUER': None,

    # Whether to include the user's ID in the token. Default is True.
    'USER_ID_FIELD': 'id',

    # The claim name for the user's ID. Default is 'user_id'.
    'USER_ID_CLAIM': 'user_id',

    # Whether to include the user's username in the token. Default is False.
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    # The claim name for the user's username. Default is 'username'.
    'AUTH_HEADER_TYPES': ('Bearer',),

    # The claim name for the token type. Default is 'token_type'.
    'TOKEN_TYPE_CLAIM': 'token_type',

    # The claim name for the expiration time. Default is 'exp'.
    'JTI_CLAIM': 'jti',

    # Whether to include the token's expiration time in the token. Default is True.
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',

    # The lifetime of the sliding token. Default is 1 day.
    'SLIDING_TOKEN_LIFETIME': timedelta(days=1),

    # The lifetime of the sliding token's refresh token. Default is 1 day.
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=7),
}

kafka_utils.create_kafka_topics(configs.get_kafka_url(), KafkaTopic)