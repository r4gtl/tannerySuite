from django.urls import path

from .views import *
                    




app_name="lavorazioni"



urlpatterns = [
    # Lavorazioni dashboard
    path("", dashboard_lavorazioni, name="dashboard_lavorazioni"),
    
    # Tabelle generiche
    path('tabelle_generiche/', tabelle_generiche, name="tabelle_generiche"),
    
    # Casuale trasporto    
    path('crea_causale_trasporto/', CausaleTrasportoCreateView.as_view(), name="crea_causale_trasporto"),
    path('modifica_causale_trasporto/<int:pk>/', CausaleTrasportoUpdateView.as_view(), name="modifica_causale_trasporto"),
    path('delete_causale_trasporto/<int:pk>/', delete_causale_trasporto, name="delete_causale_trasporto"),
    
    # Aspetto dei beni    
    path('crea_aspetto_beni/', AspettoDeiBeniCreateView.as_view(), name="crea_aspetto_beni"),
    path('modifica_aspetto_beni/<int:pk>/', AspettoDeiBeniUpdateView.as_view(), name="modifica_aspetto_beni"),
    path('delete_aspetto_beni/<int:pk>/', delete_aspetto_beni, name="delete_aspetto_beni"),
    
    # Porto materiale    
    path('crea_porto_materiale/', PortoMaterialeCreateView.as_view(), name="crea_porto_materiale"),
    path('modifica_porto_materiale/<int:pk>/', PortoMaterialeUpdateView.as_view(), name="modifica_porto_materiale"),
    path('delete_porto_materiale/<int:pk>/', delete_porto_materiale, name="delete_porto_materiale"),
    
    # Ordine di Lavoro   
    path('crea_ordine_lavoro/', OrdineLavoroCreateView.as_view(), name="crea_ordine_lavoro"),
    path('modifica_ordine_lavoro/<int:pk>/', OrdineLavoroUpdateView.as_view(), name="modifica_ordine_lavoro"),
    path('delete_ordine_lavoro/<int:pk>/', delete_ordine_lavoro, name="delete_ordine_lavoro"),

    
    
]