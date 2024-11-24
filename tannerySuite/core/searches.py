from anagrafiche.models import Fornitore
from articoli.models import Articolo, Colore, FaseLavoro, LavorazioneEsterna

from django.db.models import Q
from django.http import JsonResponse


def search_articolo(request):
    search_term = request.GET.get('search', '')
    if search_term:
        # Effettua la ricerca dell'Articolo
        articoli = Articolo.objects.filter(
            Q(descrizione__icontains=search_term)
        )
        # Costruisci il markup HTML per la tabella dei risultati della ricerca
        results_html = "<table class='table table-search'><thead><tr><th>ID</th><th>Descrizione</th></tr></thead><tbody>"
        for articolo in articoli:
            results_html += f"<tr data-id='{articolo.pk}'><td class='articolo-id'>{articolo.pk}</td><td class='articolo-descrizione'>{articolo.descrizione}</td></tr>"
        results_html += "</tbody></table>"
        
        return JsonResponse({'html': results_html})
    else:
        return JsonResponse({'html': ''})



def search_colore(request):
    search_term = request.GET.get('search', '')
    if search_term:
        # Effettua la ricerca dell'Articolo
        colori = Colore.objects.filter(
            Q(descrizione__icontains=search_term)
        )
        # Costruisci il markup HTML per la tabella dei risultati della ricerca
        results_html = "<table class='table table-search'><thead><tr><th>ID</th><th>Descrizione</th></tr></thead><tbody>"
        for colore in colori:
            results_html += f"<tr data-id='{colore.pk}'><td class='colore-id'>{colore.pk}</td><td class='colore-descrizione'>{colore.descrizione}</td></tr>"
        results_html += "</tbody></table>"
        
        return JsonResponse({'html': results_html})
    else:
        return JsonResponse({'html': ''})
    


def search_supplier(request):
    search_term = request.GET.get('search', '')
    categoria = request.GET.get('categoria', None)

    fornitori = Fornitore.objects.all()

    if search_term:
        fornitori = fornitori.filter(ragionesociale__icontains=search_term)

    if categoria:
        fornitori = fornitori.filter(categoria=categoria)

    results_html = "<table class='table table-search'><thead><tr><th>ID</th><th>RagioneSociale</th></tr></thead><tbody>"
    for fornitore in fornitori:
        results_html += f"<tr data-id='{fornitore.pk}'><td class='fornitore-id'>{fornitore.pk}</td><td class='fornitore-ragionesociale'>{fornitore.ragionesociale}</td></tr>"
    results_html += "</tbody></table>"
        
    return JsonResponse({'html': results_html})



def search_fase_lavoro(request):
    search_term = request.GET.get('search', '')
    if search_term:
        # Effettua la ricerca dei prodotti chimici
        fasi_lavoro = FaseLavoro.objects.filter(
            Q(descrizione__icontains=search_term)
        )
        # Costruisci il markup HTML per la tabella dei risultati della ricerca
        results_html = "<table class='table table-search'><thead><tr><th>ID</th><th>Fase di Lavoro</th></tr></thead><tbody>"
        for fase in fasi_lavoro:
            results_html += f"<tr data-id='{fase.pk}'><td class='fase-id'>{fase.pk}</td><td class='fase-articolo'>{fase.descrizione}</td></tr>"
        results_html += "</tbody></table>"
        
        
        return JsonResponse({'html': results_html})
    else:
        return JsonResponse({'html': ''})
    


def search_outsourcing(request):
    search_term = request.GET.get('search', '')
    if search_term:
        # Effettua la ricerca dei prodotti chimici
        lavorazioni = LavorazioneEsterna.objects.filter(
            Q(descrizione__icontains=search_term) | Q(codice__icontains=search_term)
        )
        # Costruisci il markup HTML per la tabella dei risultati della ricerca
        results_html = "<table class='table table-search'><thead><tr><th>ID</th><th>Codice</th><th>Lavorazione</th></tr></thead><tbody>"
        for lavorazione in lavorazioni:
            results_html += f"<tr data-id='{lavorazione.pk}'><td class='lavorazione-id'>{lavorazione.pk}</td><td class='lavorazione-codice'>{lavorazione.codice}</td><td class='lavorazione-descrizione'>{lavorazione.descrizione}</td></tr>"
        results_html += "</tbody></table>"
        
        
        return JsonResponse({'html': results_html})
    else:
        return JsonResponse({'html': ''})