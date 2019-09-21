"""
Django settings for qiweb project.

Generated by 'django-admin startproject' using Django 1.9.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import posixpath

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd34cbcad-ef60-428f-8bfd-ee0183ca58ec'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'app',
    # Add your apps here to enable them
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'qiweb.urls'

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

WSGI_APPLICATION = 'qiweb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOG_PATH = os.path.join(BASE_DIR, "log")
try:
    os.mkdir(LOG_PATH)
except (IOError, OSError) as e:
    pass

LOGGING = {
    "version":1,
    "disable_existing_loggers":False,
    "filters":{
        "require_debug_false":{
            "()":"django.utils.log.RequireDebugFalse"
        }
    },
    "formatters":{
        "verbose":{
            "format":"[%(loglevel)s|%(asctime)s|%(name)s] %(message)s",
            "style":"{"
        },
        "simple":{
            "format":"[%(loglevel)s|%(name)s] %(message)s",
            "style":"{"
        }
    },
    "handlers":{
        "file":{
            "level":"INFO",
            "class":"logging.handlers.RotatingFileHandler",
            "filename":os.path.join(LOG_PATH, "django.log"),
            "maxBytes":1024 * 1024 * 20,
            "backupCount":10,
            "formatter":"verbose"
        },
        "file_timed":{
            "level":"INFO",
            "class":"logging.handlers.TimedRotatingFileHandler",
            "filename":os.path.join(LOG_PATH, "django.log"),
            "when": "D",
            "interval": 1,
            "backupCount": 15,
            "formatter":"verbose"
        },
        "console":{
            "level":"INFO",
            "class":"logging.StreamHandler",
            "formatter":"simple"
        }
    },
    "loggers":{
        "qi":{
            "handlers":["file_timed", "console"],
            "level":"DEBUG",
            "filters":["require_debug_false"],
            "propagate":True
        }
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = posixpath.join(*(BASE_DIR.split(os.path.sep) + ['static']))
