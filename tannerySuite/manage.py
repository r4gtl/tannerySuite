#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import environ


def main():
    """Run administrative tasks."""
    #os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tannerySuite.settings')
     # Inizializza environ per gestire le variabili d'ambiente
    env = environ.Env()
    environ.Env.read_env()  # Legge il file .env
    
    # Imposta il modulo delle impostazioni in base alla variabile d'ambiente
    django_env = env('DJANGO_ENV', default='development')  # Usa 'development' come valore predefinito
    
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"tannerySuite.settings.{django_env}")
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
