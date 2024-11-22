import django_filters
from django import forms

from .models import Cliente, Fornitore, TransferValue


class FornitoreFilter(django_filters.FilterSet):
    
    #
    # Categoria
    NESSUNA = 'nessuna'
    PELLI = 'pelli'
    PRODOTTI_CHIMICI = 'prodotti chimici'
    LAVORAZIONI_ESTERNE = 'lavorazioni esterne'
    SERVIZI = 'servizi'
    MANUTENZIONI = 'manutenzioni'
    RIFIUTI = 'rifiuti'
    
    CHOICES_CATEGORY = (
        (NESSUNA, 'Manca categoria'),
        (PELLI, 'Pelli'),
        (PRODOTTI_CHIMICI, 'Prodotti Chimici'),
        (LAVORAZIONI_ESTERNE, 'Lavorazioni Esterne'),
        (SERVIZI, 'Servizi'),
        (MANUTENZIONI, 'Manutenzioni'),
        (RIFIUTI, 'Rifiuti'),
    )
    ragionesociale=django_filters.CharFilter(field_name='ragionesociale', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    categoria=django_filters.ChoiceFilter(choices=CHOICES_CATEGORY)
    
    class Meta:
        model = Fornitore
        fields = ['ragionesociale', 'categoria']



class ClienteFilter(django_filters.FilterSet):   
   
    ragionesociale=django_filters.CharFilter(field_name='ragionesociale', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    
    class Meta:
        model = Cliente
        fields = ['ragionesociale']



class TransferValueFilter(django_filters.FilterSet):   
   
    descrizione = django_filters.CharFilter(field_name='description', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    
    class Meta:
        model = TransferValue
        fields = ['description']