from django.urls import path

from .views import (dashboard_acquisto_pelli, tabelle_generiche_acquisto_pelli,
                    LottoCreateView, LottoUpdateView,
                    DettaglioLottoCreateView, DettaglioLottoUpdateView, delete_dettaglio_lotto,
                    SceltaLottoCreateView, SceltaLottoUpdateView, delete_scelta_lotto,
                    TipoAnimaleCreateView, TipoAnimaleUpdateView, delete_tipo_animale,
                    TipoGrezzoCreateView, TipoGrezzoUpdateView, delete_tipo_grezzo,
                    SceltaCreateView, SceltaUpdateView, delete_scelta,
                    SpessoreCreateView, SpessoreUpdateView, delete_spessore,
                    QualityCreateView, QualityUpdateView, delete_quality,
                    TaglioCreateView, TaglioUpdateView, delete_taglio,
                    SezioneCreateView, SezioneUpdateView, delete_sezione,
                    ConciaCreateView, ConciaUpdateView, delete_concia,
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

    # Dettaglio Lotto
    path('<int:pk>/crea_dettaglio_lotto/', DettaglioLottoCreateView.as_view(), name="crea_dettaglio_lotto"),
    path('modifica_dettaglio_lotto/<int:pk>/', DettaglioLottoUpdateView.as_view(), name="modifica_dettaglio_lotto"),
    path('delete_dettaglio_lotto/<int:pk>/', delete_dettaglio_lotto, name="delete_dettaglio_lotto"),
    
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
    
    # Spessore    
    path('crea_spessore/', SpessoreCreateView.as_view(), name="crea_spessore"),
    path('modifica_spessore/<int:pk>/', SpessoreUpdateView.as_view(), name="modifica_spessore"),
    path('delete_spessore/<int:pk>/', delete_spessore, name="delete_spessore"),
    
    # Quality
    path('crea_quality/', QualityCreateView.as_view(), name="crea_quality"),
    path('modifica_quality/<int:pk>/', QualityUpdateView.as_view(), name="modifica_quality"),
    path('delete_quality/<int:pk>/', delete_quality, name="delete_quality"),
    
    # Taglio
    path('crea_taglio/', TaglioCreateView.as_view(), name="crea_taglio"),
    path('modifica_taglio/<int:pk>/', TaglioUpdateView.as_view(), name="modifica_taglio"),
    path('delete_taglio/<int:pk>/', delete_taglio, name="delete_taglio"),
    
    # Sezione
    path('crea_sezione/', SezioneCreateView.as_view(), name="crea_sezione"),
    path('modifica_sezione/<int:pk>/', SezioneUpdateView.as_view(), name="modifica_sezione"),
    path('delete_sezione/<int:pk>/', delete_sezione, name="delete_sezione"),
    
    # Concia
    path('crea_concia/', ConciaCreateView.as_view(), name="crea_concia"),
    path('modifica_concia/<int:pk>/', ConciaUpdateView.as_view(), name="modifica_concia"),
    path('delete_concia/<int:pk>/', delete_concia, name="delete_concia"),

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