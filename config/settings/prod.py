from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SERVER_EMAIL = u'Магазин Powerball.ru <info@powerball.ru>'

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'powerballs',
    'USER': 'root',
    'PASSWORD': 'root',
    'HOST': '127.0.0.1',
    'PORT': '3306',
}
