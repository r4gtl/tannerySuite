import django_filters
from django import forms
from .models import RapportoAudit, RapportoNC



        
class RapportoAuditFilter(django_filters.FilterSet):
    numero_rapporto_audit = django_filters.CharFilter(lookup_expr='icontains', label='Numero')
    data_rapporto_audit = django_filters.DateFromToRangeFilter()
    
    
    class Meta:
        model = RapportoAudit
        fields = ['numero_rapporto_audit', 'data_rapporto_audit',
                
                ] 
        
class RapportoNCFilter(django_filters.FilterSet):
    numero_nc = django_filters.CharFilter(lookup_expr='icontains', label='Numero')
    data_nc = django_filters.DateFromToRangeFilter()
    tipo_nc = django_filters.ChoiceFilter(choices=RapportoNC.CHOICES_TIPO_NC)
    
    
    class Meta:
        model = RapportoNC
        fields = ['numero_nc', 'data_nc','tipo_nc',
                
                ] 