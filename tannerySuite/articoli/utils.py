
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse

from .models import (CaratteristicaProcedura, DettaglioFaseLavoro,
                     DettaglioProcedura, FaseLavoro, Procedura)


def accoda_dettaglio_fase_lavoro(request):
    if request.method == 'POST':
        fase_id = request.POST.get('fase_id')
        print(f"fase_id: {fase_id}")
        fase_attiva = request.POST.get('faseAttiva')    
        print(f"fase_attiva: {fase_attiva}")

        fase_attiva = FaseLavoro.objects.get(pk=fase_attiva) # Recupero l'istanza da passare alla FK
        # Filtro le istanze di DettaglioRicettaRifinizione in base a ricetta_id
        dettagli_fase = DettaglioFaseLavoro.objects.filter(fk_fase_lavoro=fase_id)

        # Duplico le istanze filtrate e modifico fk_ricetta_rifinizione
        for dettaglio in dettagli_fase:
            DettaglioFaseLavoro.objects.create(
                fk_fase_lavoro=fase_attiva,
                attributo=dettaglio.attributo,
                note=dettaglio.note,                
                created_by=dettaglio.created_by
            )
        
        redirect_url = reverse('articoli:modifica_fase_lavoro', kwargs={'pk': fase_attiva.pk})
        return JsonResponse({'redirect_url': redirect_url}) 
    else:
        return JsonResponse({'error': 'Richiesta non valida.'})


@transaction.atomic
def accoda_caratteristiche_fase_lavoro_dettaglio_procedura(request):
    if request.method == 'POST':
        fk_procedura = request.POST.get('fk_procedura')
        fk_faselavoro = request.POST.get('fk_faselavoro')
        print(f"dettaglio_id: {fk_faselavoro}")
        dettaglio_attivo = request.POST.get('dettaglioAttivo')    
        print(f"dettaglio_attivo: {dettaglio_attivo}")

        dettaglio_attivo = DettaglioProcedura.objects.get(pk=dettaglio_attivo) # Recupero l'istanza da passare alla FK
        
        #Elimino le istanze precedenti
        CaratteristicaProcedura.objects.filter(fk_dettaglio_procedura=dettaglio_attivo).delete()


        dettagli_fase = DettaglioFaseLavoro.objects.filter(fk_fase_lavoro=fk_faselavoro)
        for dettaglio in dettagli_fase:
            print(f"dettaglio.pk: {dettaglio.pk}" )
            print(f"dettaglio.attributo: {dettaglio.attributo}" )

        numero_riga = 0
        # Duplico le istanze filtrate e modifico fk_ricetta_rifinizione
        for dettaglio in dettagli_fase:
            numero_riga+=1
            CaratteristicaProcedura.objects.create(
                fk_dettaglio_procedura=dettaglio_attivo,  
                fk_dettaglio_fase_lavoro=dettaglio,                              
                #attributo=dettaglio.attributo,
                numero_riga=numero_riga,
                created_by=request.user
            )
        
        redirect_url = reverse('articoli:modifica_dettaglio_procedura', kwargs={'fk_procedura': fk_procedura, 'pk': dettaglio_attivo.pk})
        
        
        return JsonResponse({'redirect_url': redirect_url}) 
    else:
        return JsonResponse({'error': 'Richiesta non valida.'})