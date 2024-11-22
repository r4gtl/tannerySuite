from django.http import JsonResponse
from django.db.models import Sum, Count
import datetime

from .models import (Lotto, 
                    

                    )




# Charts
def origine_old(request):
    labels = []
    data = []
    # Calcola la data di 12 mesi fa dalla data corrente
    twelve_months_ago = datetime.datetime.now() - datetime.timedelta(days=365)
    #queryset = Lotto.objects.values('origine').annotate(lotti_count=Count('pk'))
    queryset = Lotto.objects.filter(data_acquisto__gte=twelve_months_ago).values('origine').annotate(lotti_count=Count('pk'))
    result = {
    q['origine']: q['lotti_count']
    for q in queryset
    }
    

    for entry in queryset:
        labels.append(entry['origine'])
        data.append(entry['lotti_count'])
        
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def origine_old1(request):
    labels = []
    data = []
    
    # Calcola la data di 12 mesi fa dalla data corrente
    twelve_months_ago = datetime.datetime.now() - datetime.timedelta(days=365)
    
    # Filtra i lotti con data_acquisto successiva alla data di 12 mesi fa
    queryset = Lotto.objects.filter(data_acquisto__gte=twelve_months_ago).values('origine').annotate(lotti_count=Count('pk'))
    
    result = {
        q['origine']: q['lotti_count']
        for q in queryset
    }
    

    for entry in queryset:
        labels.append(entry['origine'])
        data.append(entry['lotti_count'])
        
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
    

def origine(request):
    labels = []
    data = []
    
    # Calcola la data di 12 mesi fa dalla data corrente
    twelve_months_ago = datetime.datetime.now() - datetime.timedelta(days=365)
    
    # Filtra i lotti con data_acquisto successiva alla data di 12 mesi fa
    queryset = (
        Lotto.objects
        .filter(data_acquisto__gte=twelve_months_ago)
        .values('origine')
        .annotate(lotti_count=Count('pk'))
        .order_by('-lotti_count')  # Ordina per il numero di occorrenze in ordine decrescente
        .reverse()  # Inverte l'ordine in modo crescente
        [:10]  # Prendi solo i primi 10 record
    )
    
    result = {
        q['origine']: q['lotti_count']
        for q in queryset
    }
    
    for entry in queryset:
        labels.append(entry['origine'])
        data.append(entry['lotti_count'])
        
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


def origine_per_rpt_lwg(request):
    labels = []
    data = []
    if request.method == 'GET':
    
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        

        # Converti le date da stringhe a oggetti datetime
        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
        
        # Filtra i lotti con data_acquisto compresa tra from_date e to_date
        queryset = (
            Lotto.objects
            .filter(data_acquisto__range=[from_date, to_date])
            .values('origine')
            .annotate(lotti_count=Count('pk'))
            .order_by('-lotti_count')
            .reverse()
            [:10]
        )
        
        result = {
            q['origine']: q['lotti_count']
            for q in queryset
        }
        
        for entry in queryset:
            labels.append(entry['origine'])
            data.append(entry['lotti_count'])
            
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })       




def tipoanimale_per_rpt_lwg(request):
    labels = []
    data = []
    if request.method == 'GET':
    
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        

        # Converti le date da stringhe a oggetti datetime
        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
                
        # Filtra i lotti con data_acquisto compresa tra from_date e to_date
        queryset = (
            Lotto.objects
            .filter(data_acquisto__range=[from_date, to_date])
            .values('fk_tipoanimale__descrizione')
            .annotate(numero_pezzi=Sum('pezzi'))
            .order_by('-numero_pezzi')
            .reverse()
            [:10]
        )

        result = {
            q['fk_tipoanimale__descrizione']: q['numero_pezzi']
            for q in queryset
        }

        for entry in queryset:
            labels.append(entry['fk_tipoanimale__descrizione'])
            data.append(entry['numero_pezzi'])

        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })


def tipogrezzo_per_rpt_lwg(request):
    labels = []
    data = []
    if request.method == 'GET':
    
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        

        # Converti le date da stringhe a oggetti datetime
        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
                
        # Filtra i lotti con data_acquisto compresa tra from_date e to_date
        queryset = (
            Lotto.objects
            .filter(data_acquisto__range=[from_date, to_date])
            .values('fk_tipogrezzo__descrizione')
            .annotate(numero_pezzi=Sum('pezzi'))
            .order_by('-numero_pezzi')
            .reverse()
            [:10]
        )

        result = {
            q['fk_tipogrezzo__descrizione']: q['numero_pezzi']
            for q in queryset
        }

        for entry in queryset:
            labels.append(entry['fk_tipogrezzo__descrizione'])
            data.append(entry['numero_pezzi'])

        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })
