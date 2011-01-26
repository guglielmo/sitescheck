from settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('guglielmo', 'guglielmo.celata@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'sitescheck',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25 