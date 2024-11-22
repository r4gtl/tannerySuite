import django_filters
from django import forms
from .models import Lotto, TipoAnimale, TipoGrezzo
from anagrafiche.models import Fornitore

class LottoFilter(django_filters.FilterSet):   
   
    data_acquisto=django_filters.DateFromToRangeFilter()
    identificativo=django_filters.CharFilter(field_name='identificativo', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))
    fk_fornitore=django_filters.ModelChoiceFilter(queryset=Fornitore.objects.all(),
                                                empty_label="Tutti i Fornitori",
                                                label='Fornitore',
                                                widget=forms.Select(attrs={'class': 'form-control'})
                                                )
    fk_tipoanimale=django_filters.ModelChoiceFilter(queryset=TipoAnimale.objects.all(),
                                                empty_label="Tutti i tipi animale",
                                                label='Tipo Animale',
                                                widget=forms.Select(attrs={'class': 'form-control'})
                                                )
    fk_tipogrezzo=django_filters.ModelChoiceFilter(queryset=TipoGrezzo.objects.all(),
                                                empty_label="Tutti i tipi grezzo",
                                                label='Tipo Grezzo',
                                                widget=forms.Select(attrs={'class': 'form-control'})
                                                )
    class Meta:
        model = Lotto
        fields = ['data_acquisto', 'identificativo', 
                  'fk_fornitore', 'fk_tipoanimale', 'fk_tipogrezzo'
                  ]