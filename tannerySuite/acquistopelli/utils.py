from datetime import datetime
from django.db.models import Count, Sum
from django_countries.fields import CountryField
from .models import Lotto

# def filtro_lotti(data_inizio, data_fine):
#     lotti_filtrati = Lotto.objects.filter(data_acquisto__range=[data_inizio, data_fine])
#     return lotti_filtrati


#def filtro_lotti(data_inizio, data_fine):
#    lotti_filtrati = (
#        Lotto.objects
#        .filter(data_acquisto__range=[data_inizio, data_fine])
#        .values('fk_fornitore', 'data_acquisto', 'identificativo', 'fk_tipoanimale', 'fk_tipogrezzo')
#        .annotate(numero_lotti=Count('pk'))
#        .order_by('fk_fornitore')
#    )
#    return lotti_filtrati



def filtro_lotti_senza_totale(data_inizio, data_fine):
    lotti_filtrati = (
        Lotto.objects
        .filter(data_acquisto__range=[data_inizio, data_fine])
        .values('fk_fornitore__ragionesociale', 'data_acquisto', 'identificativo', 'fk_tipoanimale__descrizione', 'fk_tipogrezzo__descrizione', 'origine')
        .annotate(numero_lotti=Count('pk'))
        .order_by('fk_fornitore')
    )
    
    for lotto in lotti_filtrati:
        lotto['origine'] = dict(CountryField().get_choices())[lotto['origine']]
    
    return lotti_filtrati



def filtro_lotti(data_inizio, data_fine):
    lotti_filtrati = (
        Lotto.objects
        .filter(data_acquisto__range=[data_inizio, data_fine])
        .values('fk_fornitore__ragionesociale', 'fk_tipoanimale__descrizione', 'fk_tipogrezzo__descrizione', 'origine')
        .annotate(numero_lotti=Count('pk'), pezzi=Sum('pezzi'))
        .order_by('-pezzi')[:100]
    )

    for lotto in lotti_filtrati:
        lotto['origine'] = dict(CountryField().get_choices())[lotto['origine']]

    return lotti_filtrati