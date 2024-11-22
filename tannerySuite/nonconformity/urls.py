from django.urls import path
from .views import (home_rapporti_nc, home_rapporti_audit, tabelle_generiche,
                    RapportoNCCreateView, RapportoNCUpdateView, delete_rapporto_nc,
                    RapportoAuditCreateView, RapportoAuditUpdateView, delete_rapporto_audit,
                    ProcessoCreateView, ProcessoUpdateView, delete_processo,
                    ProcessoAuditCreateView, ProcessoAuditUpdateView, delete_processo_audit,
                    
                    )

from .charts import chart_nc_per_tipo_ultimo_anno


app_name="nonconformity"

urlpatterns = [
    # Home Rapporti NC
    path('', home_rapporti_nc, name='home_rapporti_nc'),

    # Rapporti NC
    path('aggiungi_rapporto_nc/', RapportoNCCreateView.as_view(), name="aggiungi_rapporto_nc"), 
    path('modifica_rapporto_nc/<int:pk>/', RapportoNCUpdateView.as_view(), name="modifica_rapporto_nc"), 
    path('delete_rapporto_nc/<int:pk>', delete_rapporto_nc, name="delete_rapporto_nc"),


    # Home Rapporti Audit
    path('home_rapporti_audit/', home_rapporti_audit, name='home_rapporti_audit'),

    # Rapporti Audit
    path('aggiungi_rapporto_audit/', RapportoAuditCreateView.as_view(), name="aggiungi_rapporto_audit"), 
    path('modifica_rapporto_audit/<int:pk>/', RapportoAuditUpdateView.as_view(), name="modifica_rapporto_audit"), 
    path('delete_rapporto_audit/<int:pk>', delete_rapporto_audit, name="delete_rapporto_audit"),

    # Tabelle Generiche
    path('tabelle_generiche/', tabelle_generiche, name='tabelle_generiche'),

    # Processi
    path('aggiungi_processo/', ProcessoCreateView.as_view(), name="aggiungi_processo"), 
    path('modifica_processo/<int:pk>/', ProcessoUpdateView.as_view(), name="modifica_processo"), 
    path('delete_processo/<int:pk>', delete_processo, name="delete_processo"),    

    # Processi-Rapporti Audit
    path('<int:fk_rapportoaudit>/aggiungi_processo_rapporto_audit/', ProcessoAuditCreateView.as_view(), name="aggiungi_processo_rapporto_audit"), 
    path('<int:fk_rapportoaudit>/modifica_processo_rapporto_audit/<int:pk>/', ProcessoAuditUpdateView.as_view(), name="modifica_processo_rapporto_audit"), 
    path('delete_processo_audit/<int:pk>', delete_processo_audit, name="delete_processo_audit"),

    # Charts
    path('chart_nc_per_tipo_ultimo_anno/', chart_nc_per_tipo_ultimo_anno, name="chart_nc_per_tipo_ultimo_anno"),

]