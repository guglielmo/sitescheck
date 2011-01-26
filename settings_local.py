from settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('guglielmo', 'guglielmo.celata@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': 'sitescheck',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025 
