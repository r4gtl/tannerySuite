from django.test import TestCase
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
    DettaglioLotto,
    Taglio,
    Sezione,
    Concia,
    TipoAnimale,
    Spessore,
    Quality,
)
from articoli.models import Lavorazione


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
