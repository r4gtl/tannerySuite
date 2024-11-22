from django.http import JsonResponse
from django.utils.dateparse import parse_date
from datetime import datetime, timedelta

from django.utils import timezone

from .models import (RapportoNC,                     

                    )





def chart_nc_per_tipo_ultimo_anno(request):
    
    today = datetime.now().date()
    from_date = today - timedelta(days=365)
    to_date = today

    
    data = RapportoNC.get_data_for_chart(from_date, to_date)
    
   

    
    # Crea un dizionario con i dati JSON
    dati_json = list(data)
        
    

    return JsonResponse(dati_json, safe=False)