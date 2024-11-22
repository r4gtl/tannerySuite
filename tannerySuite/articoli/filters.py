import django_filters
from django import forms
from .models import *

class ArticoloFilter(django_filters.FilterSet):
    descrizione=django_filters.CharFilter(lookup_expr='icontains', label='Descrizione')
    
    
    class Meta:
        model = Articolo
        fields = ['descrizione'
                ] 
        

class ColoreFilter(django_filters.FilterSet):
    descrizione=django_filters.CharFilter(lookup_expr='icontains', label='Descrizione')
    
    
    class Meta:
        model = Colore
        fields = ['descrizione'
                ] 
        

class FaseLavoroFilter(django_filters.FilterSet):
    descrizione=django_filters.CharFilter(lookup_expr='icontains', label='Descrizione')
    
    
    class Meta:
        model = FaseLavoro
        fields = ['descrizione'
                ] 
        

class ElencoTestFilter(django_filters.FilterSet):
    descrizione=django_filters.CharFilter(lookup_expr='icontains', label='Descrizione')
    
    
    class Meta:
        model = ElencoTest
        fields = ['descrizione'
                ] 
        
class LavorazioneEsternaFilter(django_filters.FilterSet):
    descrizione=django_filters.CharFilter(lookup_expr='icontains', label='Descrizione')
    
    
    class Meta:
        model = LavorazioneEsterna
        fields = ['descrizione'
                ] 