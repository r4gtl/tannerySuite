from django.urls import path

from .views import dashboard_lavorazioni, LavorazioneCreateView, LavorazioneUpdateView, delete_lavorazione
                    




app_name="lavorazioni"



urlpatterns = [
    # Lavorazioni dashboard
    path('', dashboard_lavorazioni, name="dashboard_lavorazioni"),
    
    # Lavorazione    
    path('crea_lavorazione/', LavorazioneCreateView.as_view(), name="crea_lavorazione"),
    path('modifica_lavorazione/<int:pk>/', LavorazioneUpdateView.as_view(), name="modifica_lavorazione"),
    path('delete_lavorazione/<int:pk>/', delete_lavorazione, name="delete_lavorazione"),
]