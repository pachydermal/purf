"""
Django settings for mysite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

# Parse database configuration from $DATABASE_URL
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# # Quick-start development settings - unsuitable for production
# # See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
#
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z$ep=9fspffv%#m&#d6lu$1yqhjkt@z4@q(*)+m#ep1)%)rah0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SITE_ID = 1

TEMPLATE_DEBUG = True
TEMPLATE_DIRS = (
    'templates',
    'templates/main.css',
    'templates/index.html'
)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'purf_app',
    'tastypie',
    'bootstrap3',
    'moderation',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_cas.middleware.CASMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

AUTHENTICATION_BACKENDS = (
   'django.contrib.auth.backends.ModelBackend',
   'django_cas.backends.CASBackend',
)

ROOT_URLCONF = 'purf.urls'

WSGI_APPLICATION = 'purf.wsgi.application'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'purfapp@gmail.com'
EMAIL_HOST_PASSWORD = 'kernighan'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'prof',
        'USER': 'postgres',
        'PASSWORD': 'pass',
        'HOST': '127.0.0.1',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EST'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static asset configuration
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

TEMPLATE_CONTEXT_PROCESSORS += ('purf.context_processors.getStudent','django.core.context_processors.request')

# COMMENT EVERYTHING BELOW HERE WHEN RUNNING LOCALLY
# REMEMBER TO UNCOMMENT BEFORE PUSHING!!

# CAS_SERVER_URL = 'https://fed.princeton.edu/cas/'

# LOGIN_URL = '/login/'
# # Parse database configuration from $DATABASE_URL

# import dj_database_url
# DATABASES['default'] =  dj_database_url.config()

# # Honor the 'X-Forwarded-Proto' header for request.is_secure()
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# # Allow all host headers
# ALLOWED_HOSTS = ['*']