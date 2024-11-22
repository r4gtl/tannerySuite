# your_project/settings/production.py

from .base import *

DEBUG = False

ALLOWED_HOSTS = ['192.168.1.43']
print("Production: PRODUCTION")
# Configurazioni specifiche per la produzione
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
    }
}

# Percorsi per la produzione
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Dove raccogliere i file statici in produzione
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Dove salvare i file multimediali in produzione