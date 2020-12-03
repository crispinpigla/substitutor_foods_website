from . import *

import os

SECRET_KEY = os.environ.get('SECRET_KEY', "y2!bd%d^@_)*e77o&gvgy(bndcj))ym*l_6waq%ig#!a3m6r0u")

INSTALLED_APPS = (
    'django_secrets',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}