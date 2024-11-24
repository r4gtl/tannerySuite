import django_filters
from django import forms
from .models import Lavorazione


class LavorazioneFilter(django_filters.FilterSet):   
   
    descrizione=django_filters.CharFilter(field_name='descrizione', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    codice=django_filters.CharFilter(field_name='codice', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    
    class Meta:
        model = Lavorazione
        fields = ['descrizione', 'codice',                   
                ]