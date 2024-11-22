from django.urls import path

from .utils import *
from .views import *

app_name="articoli"



urlpatterns = [

    # Home Articoli
    path("", articoli_home, name="articoli_home"),    
    path("crea_articolo/", ArticoloCreateView.as_view(), name="crea_articolo"),    
    path("modifica_articolo/<int:pk>", ArticoloUpdateView.as_view(), name="modifica_articolo"),    
    path("delete_articolo/<int:pk>", delete_articolo, name="delete_articolo"), 
    
    # Home Colori
    path("colori/", colori_home, name="colori_home"),    
    path("colori/crea_colore/", ColoreCreateView.as_view(), name="crea_colore"),    
    path("colori/modifica_colore/<int:pk>", ColoreUpdateView.as_view(), name="modifica_colore"),    
    path("colori/delete_colore/<int:pk>", delete_colore, name="delete_colore"),    
    
    # Tabelle Generiche
    path("tabelle_generiche/", tabelle_generiche, name="tabelle_generiche"),

    # Fasi di Lavoro       
    path("crea_fase_lavoro/", FaseLavoroCreateView.as_view(), name="crea_fase_lavoro"),    
    path("modifica_fase_lavoro/<int:pk>", FaseLavoroUpdateView.as_view(), name="modifica_fase_lavoro"),    
    path("delete_fase_lavoro/<int:pk>", delete_fase_lavoro, name="delete_fase_lavoro"), 

    # Attributo fasi di lavoro
    path('<int:fk_fase_lavoro>/aggiungi_attributo/', DettaglioFaseLavoroCreateView.as_view(), name="aggiungi_attributo"), 
    path('<int:fk_fase_lavoro>/modifica_attributo/<int:pk>/', DettaglioFaseLavoroUpdateView.as_view(), name="modifica_attributo"), 
    path('delete_attributo/<int:pk>', delete_dettaglio_fase_lavoro, name="delete_attributo"),
    
    # Lavorazioni Esterne      
    path("crea_lavorazione_esterna/", LavorazioneEsternaCreateView.as_view(), name="crea_lavorazione_esterna"),    
    path("modifica_lavorazione_esterna/<int:pk>", LavorazioneEsternaUpdateView.as_view(), name="modifica_lavorazione_esterna"),    
    path("delete_lavorazione_esterna/<int:pk>", delete_lavorazione_esterna, name="delete_lavorazione_esterna"), 

    # Elenco Test      
    path("crea_test/", ElencoTestCreateView.as_view(), name="crea_test"),    
    path("modifica_test/<int:pk>", ElencoTestUpdateView.as_view(), name="modifica_test"),    
    path("delete_test/<int:pk>", delete_test, name="delete_test"), 

    # Test Articolo
    path('<int:fk_articolo>/aggiungi_test_articolo/', TestArticoloCreateView.as_view(), name="aggiungi_test_articolo"), 
    path('<int:fk_articolo>/modifica_test_articolo/<int:pk>/', TestArticoloUpdateView.as_view(), name="modifica_test_articolo"), 
    path('delete_test_articolo/<int:pk>', delete_test_articolo, name="delete_test_articolo"),
    
    # Procedura
    path('<int:fk_articolo>/aggiungi_procedura/', ProceduraCreateView.as_view(), name="aggiungi_procedura"), 
    path('<int:fk_articolo>/modifica_procedura/<int:pk>/', ProceduraUpdateView.as_view(), name="modifica_procedura"), 
    path('delete_procedura/<int:pk>', delete_procedura, name="delete_procedura"),
    
    # Dettaglio Procedura
    path('<int:fk_procedura>/aggiungi_dettaglio_procedura/', DettaglioProceduraCreateView.as_view(), name="aggiungi_dettaglio_procedura"), 
    path('<int:fk_procedura>/modifica_dettaglio_procedura/<int:pk>/', DettaglioProceduraUpdateView.as_view(), name="modifica_dettaglio_procedura"), 
    path('delete_dettaglio_procedura/<int:pk>', delete_dettaglio_procedura, name="delete_dettaglio_procedura"),

    # Caratteristica Procedura
    path('<int:fk_dettaglio_procedura>/aggiungi_caratteristica_procedura/', CaratteristicaProceduraCreateView.as_view(), name="aggiungi_caratteristica_procedura"), 
    path('<int:fk_dettaglio_procedura>/modifica_caratteristica_procedura/<int:pk>/', CaratteristicaProceduraUpdateView.as_view(), name="modifica_caratteristica_procedura"), 
    path('delete_caratteristica_procedura/<int:pk>', delete_caratteristica_procedura, name="delete_caratteristica_procedura"),

    # Automatismi
    path('accoda_dettaglio_fase_lavoro/', accoda_dettaglio_fase_lavoro, name="accoda_dettaglio_fase_lavoro"),
    path('accoda_caratteristiche_fase_lavoro_dettaglio_procedura/', accoda_caratteristiche_fase_lavoro_dettaglio_procedura, name="accoda_caratteristiche_fase_lavoro_dettaglio_procedura"),

    
]