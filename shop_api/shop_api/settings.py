"""
Django settings for shop_api project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'su@9su9x8lj^x&lj+!m!(co55yk=41@m$cc+qcr!b0lis-yy*4'

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
    'rest_framework',
    'api',
    # xamin主体模块
    'xadmin',
    # xamin渲染表格模块
    'crispy_forms',
    # xamin为模型通过版本控制，可以回滚数据
    'reversion',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'api.cors.CORSMiddleware'
]
CORS_ORIGIN_ALLOW_ALL = False
from corsheaders.defaults import default_headers
CORS_ALLOW_HEADERS = list(default_headers) + [
    'Authorization',
]
CORS_ORIGIN_WHITELIST = [
	'http://localhost:8080',
    'http://127.0.0.1:8080',
    'http://3.18.144.186:80',
    'http://3.18.144.186:8080',
]

ROOT_URLCONF = 'shop_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
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

WSGI_APPLICATION = 'shop_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
# STATIC_ROOT = '/home/ubuntu/code/Shopping/shop_api/static'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

REST_FRAMEWORK = {  # 配置渲染器
    # 'DEFAULT_RENDERER_CLASSES':['rest_framework.renderers.JSONRenderer'],
    'DEFAULT_VERSIONING_CLASS':'rest_framework.versioning.QueryParameterVersioning',
    'ALLOWED_VERSIONS':['v1','v2'],
    "VERSION_PARAM":'version',
    'DEFAULT_VERSION':'v1',
    "DEFAULT_PAGINATION_CLASS": 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
    "DEFAULT_THROTTLE_RATES":{
        'user': None,
        'anon': None,
        'sms': '10/min',
    }
}
# 支付相关配置
APPID = "2016092200570009"
# 服务器异步通知页面路径 需http: // 格式的完整路径，不能加?id = 123 这类自定义参数，必须外网可以正常访问
NOTIFY_URL = "http://127.0.0.1:8001/api/v1/alipay/"
# 页面跳转同步通知页面路径 需http: // 格式的完整路径，不能加?id = 123 这类自定义参数，必须外网可以正常访问
RETURN_URL = "http://127.0.0.1:8001/api/v1/alipay/"
# 商户私钥路径
PRI_KEY_PATH = "api/keys/app_private_2048.txt"
# 支付宝公钥路径
PUB_KEY_PATH = "api/keys/alipay_public_2048.txt"

# 签名方式(当前只支持RSA和RSA2)
SIGN_TYPE = "RSA2"
# 字符编码格式
CHARSET = "utf-8"

# 支付宝网关(如果是线上环境的话, dev 这三个字去掉即可)
GATEWAY_URL_DEV = "https://openapi.alipaydev.com/gateway.do"
GATEWAY_URL = "https://openapi.alipay.com/gateway.do"

# 异步通知参数DOC(支付宝会主动发起POST请求)
# notify_doc = "https://docs.open.alipay.com/270/105902/"

# ############# 微信 ##############
WECHAT_CONFIG = {
    'app_id': 'wx5acb9aa36cc1c77f',
    'appsecret': '36e1b1bd5849d400e06e39734caa819c',
    'redirect_uri': 'http://127.0.0.1/callback/',
}


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://3.18.144.186:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
            # "PASSWORD": "密码",
        }
    }
}
SHOPPING_CAR_KEY = "luffy_shopping_car_%s_%s"
PAYMENT_KEY = "luffy_payment_%s_%s"
PAYMENT_COUPON_KEY = "luffy_payment_coupon_%s"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

AUTH_USER_MODEL = 'api.User'