import django_filters
from django import forms
from .models import Lavorazione, OrdineLavoro
from anagrafiche.models import Fornitore


class OrdineLavoroFilter(django_filters.FilterSet):   
   
    num_doc=django_filters.NumberFilter(field_name='Numero Documento', lookup_expr='icontains', widget=forms.NumberInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    data_doc = django_filters.DateFromToRangeFilter(label='Data Documento')
    fk_fornitore = django_filters.ModelChoiceFilter(
        field_name='fk_fornitore',
        queryset=Fornitore.objects.all(),
        label='Fornitore'
    )
    
    class Meta:
        model = OrdineLavoro
        fields = ['num_doc', 'data_doc', 'fk_fornitore'                   
                ]