"""
WSGI config for leatherSync project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

import environ
from django.core.wsgi import get_wsgi_application

# Inizializza environ per gestire le variabili d'ambiente
env = environ.Env()
environ.Env.read_env()  # Legge il file .env


#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leatherSync.settings')
# Imposta il modulo delle impostazioni in base alla variabile d'ambiente
django_env = env('DJANGO_ENV', default='development')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"leatherSync.settings.{django_env}")

application = get_wsgi_application()
