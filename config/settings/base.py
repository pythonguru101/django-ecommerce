import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.normpath(os.path.join(BASE_DIR, '..'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm#(pt)jf*3#)ibdd(dhk+z!n(869plw!=f)x0c*ph37bp0ruzc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_MODE = 1

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'polymorphic',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',

    'markdown',
    'markdownx',
    'imagekit',
    'pytils',
    'mptt',

    'apps.core',
    'apps.accounts',
    'apps.shop',
    'apps.main',
    'apps.banners',
    'apps.config',

    'apps.dealers',
    'apps.achievements',
    'apps.blog',
]
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'apps.shop.middleware.CartMiddleware'
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_ROOT, 'templates'),
            os.path.join(PROJECT_ROOT, 'templates%s' % TEMPLATE_MODE),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'apps.config.context_processors.app_config',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# DATABASES = {
#   'default': {
#       'ENGINE': 'django.db.backends.sqlite3',
#       'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#   }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'powerball.ru',
        'USER': 'root',
        'PASSWORD': '123456789',
        'HOST': '127.0.0.1',
        'PROT': '3306'
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'assets'),
    os.path.join(PROJECT_ROOT, 'assets%s' % TEMPLATE_MODE),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

ORDER_FORM = 'apps.shop.forms.OrderForm'

CATEGORY_MODEL = 'shop.Category'
PRODUCT_MODEL = 'shop.Product'
ORDER_MODEL = 'shop.Order'
ORDER_PRODUCTS_MODEL = 'shop.OrderProducts'

ACCOUNT_ACTIVATION_DAYS = 14

# Email settings

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'info@powerball.ru'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
