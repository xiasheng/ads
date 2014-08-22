# -*- coding: utf-8 -*-  

"""
Django settings for ads project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1iayimapuw%no6g%%6o0_79*h3x))@s@7fetjqfgmvhr14t(+n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

TEMPLATE_DIRS = (
    '/var/www/ads/ads/templates',
)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

# Application definition

INSTALLED_APPS = (
    'ads.models',
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.http.ConditionalGetMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ads.urls'

WSGI_APPLICATION = 'ads.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE':  'django.db.backends.mysql',
        'NAME': 'ads',
        'USER': 'root',
        'PASSWORD': 'd_connected',
        'HOST': '',
        'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
#LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = "/var/www/ads/ads/staticfiles/"
STATICFILES_DIRS = (
    '/var/www/ads/ads/static/',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s  %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/ads.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}


# email config
EMAIL_HOST='smtp.exmail.qq.com'
EMAIL_HOST_USER='service@d-connected.com'
EMAIL_HOST_PASSWORD='sv_456123'
EMAIL_RECIPIENTS=['xia.sheng@d-connected.com', 'zhang.shengrong@d-connected.com']
#EMAIL_RECIPIENTS=['xia.sheng@d-connected.com']

#app key
APPKEY_ANDROID = 'BOglTuO6OppR5Q5B7yQDbrF6GrO9ZECM'
APPKEY_IOS = 'AqcxTiwgD7d46vFnZ0Gh7o4BS31lGoKg'




SUIT_CONFIG = {
    # header
    'ADMIN_NAME': u'钱庄管理后台',
    'HEADER_DATE_FORMAT': 'Y/n/j  l',
    'HEADER_TIME_FORMAT': 'H:i',

    'MENU': (

        {'label': u'用户管理', 'icon':'icon-lock', 'models': ('models.user', )},

        {'label': u'数据统计', 'icon':'icon-cog', 'models': ('models.pointrecord', 'models.exchangerecord')},

        {'label': u'产品管理', 'icon':'icon-cog', 'models': ('models.exchangeproduct', 'models.channel')},
        # Separator
        '-',

    ),

    # 'LIST_PER_PAGE': 15
}

