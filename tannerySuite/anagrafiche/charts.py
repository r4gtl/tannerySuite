from django.http import JsonResponse
import json
from django.db.models import Sum, Count
from datetime import datetime
from django_countries.fields import Country

from .models import (Fornitore, Cliente
                    

                    )

def get_country_count(request):
    fornitori_per_nazione = Fornitore.objects.values('country').annotate(count=Count('country'))
    labels = [Country(f['country']).name for f in fornitori_per_nazione]
    data = [f['count'] for f in fornitori_per_nazione]
    
    chart_data = {
        'labels': labels,
        'data': data
    }
    
    return JsonResponse(chart_data)

def get_country_count_client(request):
    clienti_per_nazione = Cliente.objects.values('country').annotate(count=Count('country'))
    labels = [Country(f['country']).name for f in clienti_per_nazione]
    data = [f['count'] for f in clienti_per_nazione]
    
    chart_data = {
        'labels': labels,
        'data': data
    }
    
    return JsonResponse(chart_data)