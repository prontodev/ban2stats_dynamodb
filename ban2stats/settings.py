"""
Django settings for ban2stats project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9@xq9t3lh(6xh)ayrf(2v#8vga62)=0@b$2%7p_62#7x8cc(2='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    # 'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'attack',
)

MIDDLEWARE_CLASSES = (
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ban2stats.urls'

WSGI_APPLICATION = 'ban2stats.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'


#GEO IP Settings
GEOIP_PATH = os.path.join(BASE_DIR, 'geo_data')

BAN2STATS_SERVICE_TOKEN = 'oTbCmV71i2Lg5wQMSsPEFKGJ0Banana'
# DYNAMODB_HOST = 'http://localhost:4567'
DYNAMODB_HOST = ''
DYNAMODB_REGION = 'ap-southeast-1'
DYNAMO_MODEL_READ_CAPACITY_UNITS = 10
DYNAMO_MODEL_WRITE_CAPACITY_UNITS = 5
ATTACK_TABLE_NAME = 'Attack'
STATS_TABLE_NAME = 'Ban2Stats_Stats'
TESTING_SLEEP_TIME = 1