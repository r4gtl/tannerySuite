from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '192.168.1.43']

# Configurazioni specifiche per lo sviluppo
'''
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
'''

# Percorsi per lo sviluppo
'''STATICFILES_DIRS = [
    os.path.join(BASE_DIR.parent '/static'),  # Percorso per i file statici in sviluppo
]'''
STATICFILES_DIRS = [
    BASE_DIR.parent / 'static',  # Se 'static' è una directory a livello superiore di BASE_DIR
]
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Percorso per i file multimediali in sviluppo