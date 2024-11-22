from django.urls import path

from .charts import get_country_count, get_country_count_client
from .views import *

app_name="anagrafiche"



urlpatterns = [

    # Facility
    path("aggiungi_facility_details/", FacilityCreateView.as_view(), name="aggiungi_facility_details"),    
    path("edit_facility_details/<int:pk>", FacilityUpdateView.as_view(), name="edit_facility_details"),
    path("<int:pk>/add_facility_contact", add_facility_contact, name="add_facility_contact"),
    path("<int:pk>/modifica_facility_contact/<int:id>", FacilityContactUpdateView.as_view(), name="modifica_facility_contact"),
    path("delete_facility_contact/<int:pk>", delete_facility_contact, name="delete_facility_contact"),
    #path("<int:fk_facility>/home_autorizzazioni/", home_autorizzazioni, name="home_autorizzazioni"),
    #path("<int:fk_facility>/add_facility_authorization/", FacilityAuthorizationCreateView.as_view(), name="add_facility_authorization"),
    #path("<int:fk_facility>/modifica_facility_authorization/<int:id>", FacilityAuthorizationUpdateView.as_view(), name="modifica_facility_authorization"),
    #path("delete_facility_authorization/<int:pk>", delete_facility_authorization, name="delete_facility_authorization"),

    # Clienti
    path("home_clienti/", ListaClienteView.as_view(), name="home_clienti"),
    path("aggiungi_cliente/", ClienteCreateView.as_view(), name="aggiungi_cliente"),
    path("modifica_cliente/<int:pk>", ClienteUpdateView.as_view(), name="modifica_cliente"),
    
    # Fornitori
    path("home_fornitori/", home_fornitori, name="home_fornitori"),    
    path("aggiungi_fornitore/", CreateSupplier.as_view(), name="aggiungi_fornitore"),
    path('aggiungi_fornitore_with_category/<str:category>/', aggiungi_fornitore_with_category, name='aggiungi_fornitore_with_category'),    
    path("vedi_fornitore/<int:pk>", UpdateSupplier.as_view(), name="vedi_fornitore"),
    path("fornitore/<int:fk_fornitore>/aggiungi_lwg/", AddLwgCertificate.as_view(), name="aggiungi_lwg"),
    path("modifica_lwg/<int:pk>", UpdateLwgCertificate.as_view(), name="modifica_lwg"),    
    path("delete_lwg/<int:pk>", delete_certificato, name="delete_lwg"),
    path("modifica_lwg/<int:fk_certificato>/add_transf_value/", XrTransferValueCreateView.as_view(), name="add_transf_value"),
    path("edit_transf_value/<int:pk>", XrTransferValueUpdateView.as_view(), name="edit_transf_value"),
    path("delete_transf_value/<int:pk>", delete_xrtransfervalue, name="delete_transf_value"),

    # Listino terzisti
    path("fornitore/<int:fk_fornitore>/aggiungi_voce_listino/", ListinoTerzistaCreateView.as_view(), name="aggiungi_voce_listino"),
    path("modifica_voce_listino/<int:pk>", ListinoTerzistaUpdateView.as_view(), name="modifica_voce_listino"),    
    path("delete_voce_listino/<int:pk>", delete_voce_listino, name="delete_voce_listino"),
    
    path("<int:fk_listino_terzista>/aggiungi_prezzo_listino/", PrezzoListinoCreateView.as_view(), name="aggiungi_prezzo_listino"),
    path("modifica_prezzo_listino/<int:pk>", PrezzoListinoUpdateView.as_view(), name="modifica_prezzo_listino"),    
    path("delete_prezzo_listino/<int:pk>", delete_prezzo_listino, name="delete_prezzo_listino"),

    # Gestori Rifiuti
    path("fornitore/<int:fk_fornitore>/aggiungi_gestore_rifiuti/", XrDocumentiGestoreCreateView.as_view(), name="aggiungi_gestore_rifiuti"),
    path("modifica_gestore_rifiuti/<int:pk>", XrDocumentiGestoreUpdateView.as_view(), name="modifica_gestore_rifiuti"),    
    path("delete_gestore_rifiuti/<int:pk>", delete_gestore_rifiuti, name="delete_gestore_rifiuti"),

    # Listino Clienti
    path("cliente/<int:fk_cliente>/aggiungi_voce_listino_cliente/", ListinoClienteCreateView.as_view(), name="aggiungi_voce_listino_cliente"),
    path("modifica_voce_listino_cliente/<int:pk>", ListinoClienteUpdateView.as_view(), name="modifica_voce_listino_cliente"),    
    path("delete_voce_listino_cliente/<int:pk>", delete_voce_listino_cliente, name="delete_voce_listino_cliente"),
    
    # Tabelle Generiche
    path('tabelle_generiche/', tabelle_generiche, name="tabelle_generiche"),
    
    # Generiche - Transfer Values    
    path("add_transfer_values/", TransferValueCreateView.as_view(), name="add_transfer_values"),
    path("edit_transfer_values/<int:pk>", TransferValueUpdateView.as_view(), name="edit_transfer_values"),
    path("delete_transfer_value/<int:pk>", delete_transfer_value, name="delete_transfer_value"),

    # Charts
    path('get_country_count/', get_country_count, name='get_country_count'),
    path('get_country_count_client/', get_country_count_client, name='get_country_count_client'),
    

    
]