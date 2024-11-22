from django.urls import path

from .views import (dashboard_acquisto_pelli, tabelle_generiche_acquisto_pelli,
                    LottoCreateView, LottoUpdateView,
                    SceltaLottoCreateView, SceltaLottoUpdateView, delete_scelta_lotto,
                    TipoAnimaleCreateView, TipoAnimaleUpdateView, delete_tipo_animale,
                    TipoGrezzoCreateView, TipoGrezzoUpdateView, delete_tipo_grezzo,
                    SceltaCreateView, SceltaUpdateView, delete_scelta,
                    report_traceability_in
                    )

from .charts import (origine, 
                     origine_per_rpt_lwg, 
                     tipoanimale_per_rpt_lwg,
                     tipogrezzo_per_rpt_lwg
                     )

app_name="acquistopelli"



urlpatterns = [
    # Acquisto pelli dashboard
    path('', dashboard_acquisto_pelli, name="dashboard_acquisto_pelli"),
    path('crea_lotto/', LottoCreateView.as_view(), name="crea_lotto"),
    path('modifica_lotto/<int:pk>/', LottoUpdateView.as_view(), name="modifica_lotto"),
    path('<int:pk>/crea_scelta_lotto/', SceltaLottoCreateView.as_view(), name="crea_scelta_lotto"),
    #path('<int:pk>/modifica_scelta_lotto/<int:id>', SceltaLottoUpdateView.as_view(), name="modifica_scelta_lotto"),
    path('modifica_scelta_lotto/<int:pk>', SceltaLottoUpdateView.as_view(), name="modifica_scelta_lotto"),
    path('delete_scelta_lotto/<int:pk>', delete_scelta_lotto, name="delete_scelta_lotto"),

    
    # Tabelle generiche
    path('tabelle_generiche_acquisto_pelli/', tabelle_generiche_acquisto_pelli, name="tabelle_generiche_acquisto_pelli"),

    # Tipo animale    
    path('crea_tipo_animale/', TipoAnimaleCreateView.as_view(), name="crea_tipo_animale"),
    path('modifica_tipo_animale/<int:pk>/', TipoAnimaleUpdateView.as_view(), name="modifica_tipo_animale"),
    path('delete_tipo_animale/<int:pk>/', delete_tipo_animale, name="delete_tipo_animale"),

    # Tipo Grezzo
    path('crea_tipo_grezzo/', TipoGrezzoCreateView.as_view(), name="crea_tipo_grezzo"),
    path('modifica_tipo_grezzo/<int:pk>/', TipoGrezzoUpdateView.as_view(), name="modifica_tipo_grezzo"),
    path('delete_tipo_grezzo/<int:pk>/', delete_tipo_grezzo, name="delete_tipo_grezzo"),

    # Scelta
    path('crea_scelta/', SceltaCreateView.as_view(), name="crea_scelta"),
    path('modifica_scelta/<int:pk>/', SceltaUpdateView.as_view(), name="modifica_scelta"),
    path('delete_scelta/<int:pk>/', delete_scelta, name="delete_scelta"),


    # Charts
    path('origine/', origine, name='origine'),
    path('origine_per_rpt_lwg/', origine_per_rpt_lwg, name='origine_per_rpt_lwg'),
    path('tipoanimale_per_rpt_lwg/', tipoanimale_per_rpt_lwg, name='tipoanimale_per_rpt_lwg'),
    path('tipogrezzo_per_rpt_lwg/', tipogrezzo_per_rpt_lwg, name='tipogrezzo_per_rpt_lwg'),

    # Stampe
    path('report_traceability_in/', report_traceability_in, name='report_traceability_in'),

]