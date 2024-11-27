from django.urls import path


from .views import *
from .searches import *
from .utils import carica_destinazioni

app_name="core"



urlpatterns = [

    # Facility
    

    # Clienti
    
    
    # Fornitori
    #path("home_fornitori/", home_fornitori, name="home_fornitori"),    
    # Ricerche
    path('search_articolo/', search_articolo, name='search_articolo'),
    path('search_colore/', search_colore, name='search_colore'),
    path('search_supplier/', search_supplier, name='search_supplier'),
    path('search_outsourcing/', search_outsourcing, name='search_outsourcing'),
    path('search_fase_lavoro/', search_fase_lavoro, name="search_fase_lavoro"), # Fase lavoro
    
    path('carica_destinazioni/', carica_destinazioni, name='carica_destinazioni'),

    
]