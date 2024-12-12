from django.test import TestCase, Client
from unittest.mock import patch
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
from decimal import Decimal
from .models import (
    Articolo,
    Colore,
    FaseLavoro,
    DettaglioFaseLavoro,
    Lavorazione,
    Procedura,
    DettaglioProcedura,
    CaratteristicaProcedura,
    ElencoTest,
    TestArticolo,
    ListinoTerzista,
    PrezzoListino,
    ListinoCliente,
)
from anagrafiche.models import Fornitore, Cliente


class ModelsTestCase(TestCase):
    def setUp(self):
        # Creazione di un utente
        self.user = User.objects.create_user(username="testuser", password="12345")

        # Creazione di Fornitore e Cliente
        self.fornitore = Fornitore.objects.create(
            ragionesociale="Fornitore 1", created_by=self.user  # Associa l'utente
        )
        self.cliente = Cliente.objects.create(
            ragionesociale="Cliente 1", created_by=self.user  # Associa l'utente
        )

        # Creazione di un Articolo
        self.articolo = Articolo.objects.create(
            descrizione="Articolo 1",
            industries_served=Articolo.AUTOMOTIVE,
            note="Note sull'articolo",
            created_by=self.user,
        )

        # Creazione di una Lavorazione
        self.lavorazione = Lavorazione.objects.create(
            descrizione="Lavorazione 1",
            codice="COD123",
            note="Note sulla lavorazione",
            created_by=self.user,
        )

        # Creazione di un ElencoTest
        self.test = ElencoTest.objects.create(
            descrizione="Test di resistenza",
            norma_riferimento="ISO123",
            note="Note sul test",
            created_by=self.user,
        )

        # Creazione di una FaseLavoro
        self.fase_lavoro = FaseLavoro.objects.create(
            descrizione="Fase Interna",
            interno_esterno=FaseLavoro.INTERNO,
            um=FaseLavoro.MQ,
            note="Note sulla fase di lavoro",
            created_by=self.user,
        )

    def test_articolo_creation(self):
        self.assertEqual(self.articolo.descrizione, "Articolo 1")
        self.assertEqual(self.articolo.industries_served, Articolo.AUTOMOTIVE)
        self.assertEqual(str(self.articolo), "Articolo 1")

    def test_lavorazione_creation(self):
        self.assertEqual(self.lavorazione.descrizione, "Lavorazione 1")
        self.assertEqual(self.lavorazione.codice, "COD123")
        self.assertEqual(str(self.lavorazione), "Lavorazione 1")

    def test_elenco_test_creation(self):
        self.assertEqual(self.test.descrizione, "Test di resistenza")
        self.assertEqual(self.test.norma_riferimento, "ISO123")
        self.assertEqual(str(self.test), "Test di resistenza")

    def test_fase_lavoro_creation(self):
        self.assertEqual(self.fase_lavoro.descrizione, "Fase Interna")
        self.assertEqual(self.fase_lavoro.interno_esterno, FaseLavoro.INTERNO)
        self.assertEqual(self.fase_lavoro.um, FaseLavoro.MQ)
        self.assertEqual(str(self.fase_lavoro), "Fase Interna")

    def test_procedura_creation(self):
        procedura = Procedura.objects.create(
            fk_articolo=self.articolo,
            nr_procedura=1,
            nr_revisione=1,
            note="Note sulla procedura",
            created_by=self.user,
        )
        self.assertEqual(procedura.nr_procedura, 1)
        self.assertEqual(procedura.nr_revisione, 1)
        self.assertEqual(
            str(procedura),
            f"{self.articolo} Procedura Nr. 1 del {procedura.data_procedura} Revisione nr. 1 del {procedura.data_revisione}",
        )

    def test_listino_cliente_creation(self):
        listino = ListinoCliente.objects.create(
            fk_cliente=self.cliente,
            fk_articolo=self.articolo,
            prezzo=100.5,
            note="Note sul listino",
            created_by=self.user,
        )
        self.assertEqual(listino.fk_cliente, self.cliente)
        self.assertEqual(listino.fk_articolo, self.articolo)
        self.assertEqual(listino.prezzo, 100.5)
        self.assertEqual(str(listino), "Articolo 1")

    def test_listino_terzista_ultimo_prezzo(self):
        listino = ListinoTerzista.objects.create(
            fk_fornitore=self.fornitore,
            fk_lavorazione=self.lavorazione,
            note="Note sul listino",
            created_by=self.user,
        )
        PrezzoListino.objects.create(
            fk_listino_terzista=listino,
            data_inserimento=date(2023, 1, 1),
            prezzo=50.0,
            note="Prezzo iniziale",
            created_by=self.user,
        )
        PrezzoListino.objects.create(
            fk_listino_terzista=listino,
            data_inserimento=date(2023, 1, 2),
            prezzo=60.0,
            note="Prezzo aggiornato",
            created_by=self.user,
        )
        self.assertEqual(listino.ultimo_prezzo, Decimal("60.000"))


class FunctionTests(TestCase):
    def setUp(self):
        # Creazione utente
        self.user = User.objects.create_user(username="testuser", password="12345")

        # Creazione dati per Articolo
        self.articolo = Articolo.objects.create(
            descrizione="Articolo 1",
            industries_served=Articolo.AUTOMOTIVE,
            created_by=self.user,
        )

        # Creazione dati per FaseLavoro e DettaglioFaseLavoro
        self.fase_lavoro1 = FaseLavoro.objects.create(
            descrizione="Fase Lavoro 1", created_by=self.user
        )
        self.fase_lavoro2 = FaseLavoro.objects.create(
            descrizione="Fase Lavoro 2", created_by=self.user
        )

        DettaglioFaseLavoro.objects.create(
            fk_fase_lavoro=self.fase_lavoro1,
            attributo="Attributo 1",
            note="Nota 1",
            created_by=self.user,
        )

        # Creazione dati per Procedura e DettaglioProcedura
        self.procedura = Procedura.objects.create(
            fk_articolo=self.articolo,
            nr_procedura=1,
            nr_revisione=1,
            created_by=self.user,
        )
        self.dettaglio_procedura = DettaglioProcedura.objects.create(
            fk_procedura=self.procedura,
            fk_faselavoro=self.fase_lavoro1,
            numero_riga=1,
            created_by=self.user,
        )

        self.client = Client()
        self.client.force_login(self.user)

    def test_accoda_dettaglio_fase_lavoro(self):
        url = reverse("articoli:accoda_dettaglio_fase_lavoro")
        data = {
            "fase_id": self.fase_lavoro1.pk,
            "faseAttiva": self.fase_lavoro2.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("redirect_url", response.json())

        # Verifica duplicazione
        dettagli_fase = DettaglioFaseLavoro.objects.filter(
            fk_fase_lavoro=self.fase_lavoro2
        )
        self.assertEqual(dettagli_fase.count(), 1)
        self.assertEqual(dettagli_fase.first().attributo, "Attributo 1")

    def test_accoda_caratteristiche_fase_lavoro_dettaglio_procedura(self):
        url = reverse("articoli:accoda_caratteristiche_fase_lavoro_dettaglio_procedura")
        data = {
            "fk_procedura": self.procedura.pk,
            "fk_faselavoro": self.fase_lavoro1.pk,
            "dettaglioAttivo": self.dettaglio_procedura.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("redirect_url", response.json())

        # Verifica eliminazione e duplicazione
        caratteristiche = CaratteristicaProcedura.objects.filter(
            fk_dettaglio_procedura=self.dettaglio_procedura
        )
        self.assertEqual(caratteristiche.count(), 1)
        self.assertEqual(
            caratteristiche.first().fk_dettaglio_fase_lavoro,
            DettaglioFaseLavoro.objects.first(),
        )

    def test_accoda_dettaglio_fase_lavoro_fase_attiva_non_esistente(self):
        url = reverse("articoli:accoda_dettaglio_fase_lavoro")
        data = {
            "fase_id": self.fase_lavoro1.pk,
            "faseAttiva": 9999,  # ID inesistente
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertEqual(response.json()["error"], "Fase attiva non trovata.")

    def test_accoda_caratteristiche_fase_lavoro_dettaglio_attivo_non_esistente(self):
        url = reverse("articoli:accoda_caratteristiche_fase_lavoro_dettaglio_procedura")
        data = {
            "fk_procedura": self.procedura.pk,
            "fk_faselavoro": self.fase_lavoro1.pk,
            "dettaglioAttivo": 9999,  # ID inesistente
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertEqual(response.json()["error"], "Dettaglio attivo non trovato.")

    @patch("articoli.models.CaratteristicaProcedura.objects.filter")
    def test_eliminazione_mock(self, mock_filter):
        mock_queryset = mock_filter.return_value
        mock_queryset.delete.return_value = None  # Simula la chiamata delete()

        url = reverse("articoli:accoda_caratteristiche_fase_lavoro_dettaglio_procedura")
        data = {
            "fk_procedura": self.procedura.pk,
            "fk_faselavoro": self.fase_lavoro1.pk,
            "dettaglioAttivo": self.dettaglio_procedura.pk,
        }
        response = self.client.post(url, data)

        # Verifica che il mock sia stato chiamato
        mock_filter.assert_called_with(fk_dettaglio_procedura=self.dettaglio_procedura)
        mock_queryset.delete.assert_called_once()
        self.assertEqual(response.status_code, 200)

    def test_save_without_fk_articolo(self):
        procedura = Procedura(nr_procedura=1, nr_revisione=1, created_by=self.user)
        with self.assertRaises(ValidationError) as context:
            procedura.save()
        self.assertIn(
            "fk_articolo è obbligatorio per salvare una Procedura.",
            str(context.exception),
        )
