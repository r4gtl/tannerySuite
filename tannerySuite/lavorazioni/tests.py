from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date, time
from .models import (
    CausaleTrasporto,
    AspettoDeiBeni,
    PortoMateriale,
    UnitaMisura,
    OrdineLavoro,
    DettaglioOrdineLavoro,
    OutputLavorazione,
)
from anagrafiche.models import Fornitore, DestinazioneDiversaFornitore
from acquistopelli.models import (
    Lotto,
    DettaglioLotto,
    Taglio,
    Sezione,
    Concia,
    TipoAnimale,
    Spessore,
    Quality,
)
from articoli.models import Lavorazione

from lavorazioni.forms import RicercaLottoForm


class ModelsTestCase(TestCase):

    def setUp(self):
        # Create User
        self.user = User.objects.create_user(username="testuser", password="12345")

        # Create Fornitore and related data
        self.fornitore = Fornitore.objects.create(ragionesociale="Fornitore1")
        self.destinazione_diversa = DestinazioneDiversaFornitore.objects.create(
            fk_fornitore=self.fornitore, ragionesociale="Destinazione1"
        )

        # Create related model instances for testing
        self.causale_trasporto = CausaleTrasporto.objects.create(
            descrizione="Causale 1", note="Test note", created_by=self.user
        )

        self.aspetto_dei_beni = AspettoDeiBeni.objects.create(
            descrizione="Aspetto 1", note="Test note", created_by=self.user
        )

        self.unita_misura = UnitaMisura.objects.create(
            descrizione="Kg", abbreviazione="kg", created_by=self.user
        )

    def test_causale_trasporto_creation(self):
        # Test if the instance is created correctly
        self.assertEqual(self.causale_trasporto.descrizione, "Causale 1")
        self.assertEqual(self.causale_trasporto.created_by, self.user)
        self.assertEqual(str(self.causale_trasporto), "Causale 1")

    def test_aspetto_dei_beni_creation(self):
        # Test AspettoDeiBeni instance
        self.assertEqual(self.aspetto_dei_beni.descrizione, "Aspetto 1")
        self.assertEqual(str(self.aspetto_dei_beni), "Aspetto 1")

    def test_unita_misura_creation(self):
        # Test UnitaMisura instance
        self.assertEqual(self.unita_misura.abbreviazione, "kg")
        self.assertEqual(str(self.unita_misura), "kg")

    def test_ordine_lavoro_creation(self):
        ordine = OrdineLavoro.objects.create(
            int_est=OrdineLavoro.INTERNO,
            num_doc=123,
            data_doc=date.today(),
            fk_fornitore=self.fornitore,
            fk_causale_trasporto=self.causale_trasporto,
            trasporto=OrdineLavoro.MITTENTE,
            data_inizio_trasporto=date.today(),
            ora_inizio_trasporto=time(10, 30),
            fk_aspetto_beni=self.aspetto_dei_beni,
            peso_kg=150.5,
            created_by=self.user,
        )
        self.assertEqual(ordine.num_doc, 123)
        self.assertEqual(ordine.fk_fornitore, self.fornitore)
        self.assertEqual(ordine.trasporto, OrdineLavoro.MITTENTE)

    def test_dettaglio_ordine_lavoro_creation(self):
        ordine = OrdineLavoro.objects.create(
            int_est=OrdineLavoro.INTERNO,
            num_doc=123,
            data_doc=date.today(),
            fk_fornitore=self.fornitore,
            fk_causale_trasporto=self.causale_trasporto,
            trasporto=OrdineLavoro.MITTENTE,
            data_inizio_trasporto=date.today(),
            ora_inizio_trasporto=time(10, 30),
            fk_aspetto_beni=self.aspetto_dei_beni,
            peso_kg=150.5,
            created_by=self.user,
        )
        dettaglio = DettaglioOrdineLavoro.objects.create(
            numero_riga=1,
            fk_ordine_lavoro=ordine,
            descrizione="Test Dettaglio",
            quantity=10,
            created_by=self.user,
        )
        self.assertEqual(dettaglio.numero_riga, 1)
        self.assertEqual(dettaglio.fk_ordine_lavoro, ordine)


class RicercaLottoViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Creazione degli oggetti per i campi ForeignKey
        fornitore = Fornitore.objects.create(ragionesociale="Fornitore Test")

        # Creazione degli oggetti correlati per le ForeignKey
        tipo_animale = TipoAnimale.objects.create(descrizione="Bovino")
        spessore = Spessore.objects.create(descrizione="1.5mm")
        quality = Quality.objects.create(descrizione="Alta")
        taglio = Taglio.objects.create(descrizione="Taglio Test")
        sezione = Sezione.objects.create(descrizione="Sezione Test")
        concia = Concia.objects.create(descrizione="Concia Test")

        # Creazione dell'oggetto Lotto
        Lotto.objects.create(
            data_acquisto="2024-12-01",
            identificativo="1234",
            fk_fornitore=fornitore,
            fk_taglio=taglio,
            fk_sezione=sezione,
            fk_concia=concia,
            fk_tipoanimale=tipo_animale,
            fk_spessore=spessore,
            fk_quality=quality,
            origine="IT",
            documento="DOC001",
            peso_totale=150.25,
            pezzi=10,
            prezzo_unitario=20.5,
            spese_accessorie=50.0,
            kg_km=3000,
            note="Lotto di test",
            created_by=None,  # O specifica un utente se necessario
        )

    def test_ricerca_lotto_view_get(self):
        # Testare la visualizzazione iniziale della pagina di ricerca
        response = self.client.get(reverse("lavorazioni:ricerca_lotto"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lavorazioni/ricerca_lotto.html")
        self.assertIn("form_ricerca", response.context)

    def test_ricerca_lotto_view_post(self):
        # Testare la ricerca con parametri specifici
        form_data = {
            "identificativo": "1234",
            "fornitore": Fornitore.objects.first().pk,
            "taglio": "",
            "sezione": "",
            "concia": "",
            "tipoanimale": TipoAnimale.objects.first().pk,
            "spessore": "",
            "quality": "",
        }
        response = self.client.post(reverse("lavorazioni:ricerca_lotto"), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lavorazioni/risultati_ricerca_lotto.html")
        self.assertIn("lotti", response.context)
        self.assertEqual(len(response.context["lotti"]), 1)  # Deve filtrare un lotto

    def test_ricerca_lotto_view_post_invalid(self):
        # Testare la gestione di una form non valida
        response = self.client.post(reverse("lavorazioni:ricerca_lotto"), {})
        self.assertEqual(response.status_code, 200)  # Mostra la pagina originale
        self.assertTemplateUsed(response, "lavorazioni/risultati_ricerca_lotto.html")
        self.assertIn("form_ricerca", response.context)

    def test_ricerca_lotto_modal_view(self):
        # Testare la visualizzazione del modal
        response = self.client.get(reverse("lavorazioni:ricerca_lotto_modal"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lavorazioni/modals/modal_ricerca_lotto.html")
        self.assertIn("form_ricerca", response.context)
