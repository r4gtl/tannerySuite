from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date
from decimal import Decimal
from .models import (
    Articolo, Colore, FaseLavoro, DettaglioFaseLavoro, Lavorazione,
    Procedura, DettaglioProcedura, CaratteristicaProcedura, ElencoTest,
    TestArticolo, ListinoTerzista, PrezzoListino, ListinoCliente
)
from anagrafiche.models import Fornitore, Cliente


class ModelsTestCase(TestCase):
    def setUp(self):
        # Creazione di un utente
        self.user = User.objects.create_user(username="testuser", password="12345")
        
        # Creazione di Fornitore e Cliente
        self.fornitore = Fornitore.objects.create(
            ragionesociale="Fornitore 1",
            created_by=self.user  # Associa l'utente
        )
        self.cliente = Cliente.objects.create(
            ragionesociale="Cliente 1",
            created_by=self.user  # Associa l'utente
        )
        
        # Creazione di un Articolo
        self.articolo = Articolo.objects.create(
            descrizione="Articolo 1",
            industries_served=Articolo.AUTOMOTIVE,
            note="Note sull'articolo",
            created_by=self.user
        )
        
        # Creazione di una Lavorazione
        self.lavorazione = Lavorazione.objects.create(
            descrizione="Lavorazione 1",
            codice="COD123",
            note="Note sulla lavorazione",
            created_by=self.user
        )
        
        # Creazione di un ElencoTest
        self.test = ElencoTest.objects.create(
            descrizione="Test di resistenza",
            norma_riferimento="ISO123",
            note="Note sul test",
            created_by=self.user
        )
        
        # Creazione di una FaseLavoro
        self.fase_lavoro = FaseLavoro.objects.create(
            descrizione="Fase Interna",
            interno_esterno=FaseLavoro.INTERNO,
            um=FaseLavoro.MQ,
            note="Note sulla fase di lavoro",
            created_by=self.user
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
            created_by=self.user
        )
        self.assertEqual(procedura.nr_procedura, 1)
        self.assertEqual(procedura.nr_revisione, 1)
        self.assertEqual(str(procedura), f'{self.articolo} Procedura Nr. 1 del {procedura.data_procedura} Revisione nr. 1 del {procedura.data_revisione}')
        
    def test_listino_cliente_creation(self):
        listino = ListinoCliente.objects.create(
            fk_cliente=self.cliente,
            fk_articolo=self.articolo,
            prezzo=100.5,
            note="Note sul listino",
            created_by=self.user
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
            created_by=self.user
        )
        PrezzoListino.objects.create(
            fk_listino_terzista=listino,
            data_inserimento=date(2023, 1, 1),
            prezzo=50.0,
            note="Prezzo iniziale",
            created_by=self.user
        )
        PrezzoListino.objects.create(
            fk_listino_terzista=listino,
            data_inserimento=date(2023, 1, 2),
            prezzo=60.0,
            note="Prezzo aggiornato",
            created_by=self.user
        )
        self.assertEqual(listino.ultimo_prezzo, Decimal('60.000'))
