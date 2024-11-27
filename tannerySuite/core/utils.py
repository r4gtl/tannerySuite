from django.http import JsonResponse
from anagrafiche.models import DestinazioneDiversaFornitore

def carica_destinazioni(request):
    fornitore_id = request.GET.get('fk_fornitore')
    if fornitore_id:
        try:
            destinazioni = DestinazioneDiversaFornitore.objects.filter(fk_fornitore=fornitore_id)
            data = [{'id': d.id, 'ragionesociale': d.ragionesociale} for d in destinazioni]  # Adatta il campo 'nome' se diverso
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'fornitore_id non fornito'}, status=400)