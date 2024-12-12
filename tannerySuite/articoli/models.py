from datetime import date
from django.core.exceptions import ValidationError

# from acquistopelli.models import TipoAnimale, TipoGrezzo
from anagrafiche.models import Fornitore, Cliente
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max
from django.utils import timezone


class Articolo(models.Model):
    # Industrie fornite
    APPAREL_CLOTHING = "apparel/clothing"
    AUTOMOTIVE = "automotive"
    CONTRACT = "contract"
    FOOTWEAR = "footwear"
    FOOTWEAR_ATHLETIC = "footwear (athletic)"
    LEATHER_GOODS = "leather goods"
    UPHOLSTERY = "upholstery"

    CHOICES_INDUSTRIES_SERVED = (
        (APPAREL_CLOTHING, "Apparel/clothing"),
        (AUTOMOTIVE, "Automotive"),
        (CONTRACT, "Contract"),
        (FOOTWEAR, "Footwear"),
        (FOOTWEAR_ATHLETIC, "Footwear (Athletic)"),
        (LEATHER_GOODS, "Leather goods"),
        (UPHOLSTERY, "Upholstery"),
    )

    descrizione = models.CharField(max_length=100)
    scheda_tecnica = models.FileField(
        upload_to="schede_tecniche_articoli/", null=True, blank=True
    )
    industries_served = models.CharField(
        max_length=50, choices=CHOICES_INDUSTRIES_SERVED, null=True, blank=True
    )
    # fk_tipoanimale = models.ForeignKey(TipoAnimale, null=True, blank=True, on_delete=models.SET_NULL, related_name='articolo')
    # fk_tipogrezzo = models.ForeignKey(TipoGrezzo, null=True, blank=True, on_delete=models.SET_NULL, related_name='articolo')
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User, related_name="articolo", null=True, blank=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "articoli"

    def __str__(self):
        return self.descrizione


class Colore(models.Model):
    descrizione = models.CharField(max_length=100)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User, related_name="colore", null=True, blank=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "colori"

    def __str__(self):
        return self.descrizione


class FaseLavoro(models.Model):

    # Interno/Esterno
    INTERNO = "interno"
    ESTERNO = "esterno"

    CHOICES_INT_EST = ((INTERNO, "Interno"), (ESTERNO, "Esterno"))

    # Unità di misura
    MQ = "mq"
    NUMERO = "Nr."
    PESO_KG = "Kg."

    CHOICES_UM = (
        (MQ, "Mq."),
        (NUMERO, "Nr."),
        (PESO_KG, "Kg."),
    )
    descrizione = models.CharField(max_length=100)
    interno_esterno = models.CharField(
        max_length=10, choices=CHOICES_INT_EST, null=True, blank=True
    )
    um = models.CharField(max_length=100, choices=CHOICES_UM, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name="faselavoro",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "fasi lavoro"

    def __str__(self):
        return self.descrizione


class DettaglioFaseLavoro(models.Model):
    fk_fase_lavoro = models.ForeignKey(FaseLavoro, on_delete=models.CASCADE)
    attributo = models.CharField(max_length=100)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name="dettagliofaselavoro",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.attributo


class Lavorazione(models.Model):
    descrizione = models.CharField(max_length=200)
    codice = models.CharField(max_length=9)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name="lavorazione",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.descrizione

    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "Lavorazioni"


'''
class LavorazioneEsterna(models.Model):
    descrizione = models.CharField(max_length=200)
    codice = models.CharField(max_length=9)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='lavorazione_esterna', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.descrizione
    
    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "Lavorazioni esterne"'''


class Procedura(models.Model):
    fk_articolo = models.ForeignKey(Articolo, on_delete=models.CASCADE)
    nr_procedura = models.IntegerField(blank=True, null=True)
    data_procedura = models.DateField(default=timezone.now)
    nr_revisione = models.IntegerField(blank=True, null=True)
    data_revisione = models.DateField(default=timezone.now)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User, related_name="procedure", null=True, blank=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not getattr(
            self, "fk_articolo", None
        ):  # Usa getattr per evitare RelatedObjectDoesNotExist
            raise ValidationError(
                "fk_articolo è obbligatorio per salvare una Procedura."
            )

    def save(self, *args, **kwargs):

        # Chiamata a clean per eseguire la validazione
        self.clean()

        # Se il numero ricetta è vuoto
        if self.nr_procedura is None:
            max_nr_procedura = Procedura.objects.aggregate(Max("nr_procedura"))[
                "nr_procedura__max"
            ]
            if self.pk:
                # Stai modificando una ricetta esistente
                previous_instance = Procedura.objects.get(pk=self.pk)
                print("Previous instance: " + str(previous_instance))
                if self.fk_articolo != previous_instance.fk_articolo:
                    # L'articolo è stato cambiato, controlla se esiste già una ricetta per il nuovo articolo
                    # existing_ricetta = RicettaRifinizione.objects.filter(
                    #    fk_articolo=self.fk_articolo
                    # ).exclude(pk=self.pk).order_by('-numero_revisione').first()

                    existing_procedura = (
                        Procedura.objects.filter(fk_articolo=self.fk_articolo)
                        .order_by("-nr_revisione")
                        .first()
                    )
                    print("Articolo: " + str(self.fk_articolo))
                    print("Ricetta: " + str(existing_procedura))

                    if existing_procedura:
                        print(
                            f"Modifica: la procedura esiste. Existing ricetta numero ricetta: {existing_procedura.nr_procedura} | Existing ricetta data ricetta: {existing_procedura.data_ricetta} existing_procedura.numero_revisione: {existing_procedura.nr_revisione}"
                        )
                        # Esiste già una ricetta per il nuovo articolo, quindi usa il suo numero di ricetta
                        self.nr_procedura = existing_procedura.nr_procedura
                        self.data_procedura = existing_procedura.data_procedura
                        self.nr_revisione = existing_procedura.nr_revisione + 1
                    else:
                        print(
                            "Modifica: la procedura NON esiste. Existing procedura numero riproceduracetta: "
                            + str(existing_procedura.nr_procedura)
                            + "existing_procedura.numero_revisione: "
                            + str(existing_procedura.nr_revisione)
                        )
                        # Non esiste ancora una ricetta per il nuovo articolo, quindi incrementa solo il numero_revisione
                        self.nr_procedura = (
                            max_nr_procedura + 1 if max_nr_procedura else 1
                        )
                        self.nr_revisione = previous_instance.nr_revisione + 1
            else:
                # Stai creando una nuova ricetta

                # Stai creando una nuova ricetta
                existing_procedura = (
                    Procedura.objects.filter(fk_articolo=self.fk_articolo)
                    .order_by("-nr_revisione")
                    .first()
                )
                print("Articolo: " + str(self.fk_articolo))
                print("Ricetta: " + str(existing_procedura))
                # existing_ricetta = RicettaRifinizione.objects.order_by('-numero_revisione').first()

                if existing_procedura:
                    print(
                        "Creazione: la procedura esiste. Existing procedura numero procedura: "
                        + str(existing_procedura.nr_procedura)
                        + "existing_procedura.nr_revisione: "
                        + str(existing_procedura.nr_revisione)
                    )
                    # Esiste già una ricetta, quindi usa il suo numero di ricetta e incrementa solo il numero_revisione
                    self.nr_procedura = existing_procedura.nr_procedura
                    self.data_procedura = existing_procedura.data_procedura
                    self.nr_revisione = existing_procedura.nr_revisione + 1
                else:
                    # Non esiste ancora una ricetta, quindi inizia con il numero 1 per entrambi
                    self.nr_procedura = max_nr_procedura + 1 if max_nr_procedura else 1
                    # self.numero_ricetta = 1
                    self.nr_revisione = 1
                    # print("Creazione: la ricetta NON esiste. Existing ricetta numero ricetta: " + str(self.numero_ricetta) + "existing_ricetta.numero_revisione: " + str(self.numero_revisione))
        else:
            # Se il numero ricetta non è vuoto
            max_nr_procedura = Procedura.objects.aggregate(Max("nr_procedura"))[
                "nr_procedura__max"
            ]
            if self.pk:
                # Stai modificando una ricetta esistente
                previous_instance = Procedura.objects.get(pk=self.pk)
                print("Previous instance: " + str(previous_instance))
                if self.fk_articolo != previous_instance.fk_articolo:
                    existing_procedura = (
                        Procedura.objects.filter(fk_articolo=self.fk_articolo)
                        .order_by("-nr_revisione")
                        .first()
                    )

                    if existing_procedura:
                        # Esiste già una ricetta per il nuovo articolo, quindi usa il suo numero di ricetta
                        self.nr_procedura = existing_procedura.nr_procedura
                        self.nr_revisione = existing_procedura.nr_revisione + 1
                    else:

                        # Non esiste ancora una ricetta per il nuovo articolo, quindi incrementa solo il numero_revisione
                        self.nr_procedura = (
                            max_nr_procedura + 1 if max_nr_procedura else 1
                        )
                        self.nr_revisione = previous_instance.nr_revisione + 1
            else:
                # Stai creando una nuova ricetta
                existing_procedura = (
                    Procedura.objects.filter(fk_articolo=self.fk_articolo)
                    .order_by("-nr_revisione")
                    .first()
                )

                if existing_procedura:
                    # Esiste già una ricetta, quindi usa il suo numero di ricetta e incrementa solo il numero_revisione
                    self.nr_procedura = existing_procedura.nr_procedura
                    self.nr_revisione = existing_procedura.nr_revisione + 1
                else:
                    # Non esiste ancora una ricetta, quindi inizia con il numero 1 per entrambi
                    self.nr_procedura = max_nr_procedura + 1 if max_nr_procedura else 1
                    self.nr_revisione = 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.fk_articolo} Procedura Nr. {self.nr_procedura} del {self.data_procedura} Revisione nr. {self.nr_revisione} del {self.data_revisione}"


class DettaglioProcedura(models.Model):
    fk_procedura = models.ForeignKey(Procedura, on_delete=models.CASCADE)
    fk_faselavoro = models.ForeignKey(FaseLavoro, on_delete=models.CASCADE)
    fk_fornitore = models.ForeignKey(
        Fornitore, on_delete=models.CASCADE, null=True, blank=True
    )
    is_interna = models.BooleanField(default=True)
    numero_riga = models.IntegerField()
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name="dettaglioprocedura",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["numero_riga"]
        verbose_name_plural = "dettaglio procedure"


class CaratteristicaProcedura(models.Model):
    fk_dettaglio_procedura = models.ForeignKey(
        DettaglioProcedura,
        related_name="caratteristicaprocedura",
        on_delete=models.CASCADE,
    )
    fk_fornitore = models.ForeignKey(
        Fornitore,
        on_delete=models.CASCADE,
        related_name="caratteristicaprocedura",
        null=True,
        blank=True,
    )
    fk_dettaglio_fase_lavoro = models.ForeignKey(
        DettaglioFaseLavoro,
        on_delete=models.CASCADE,
        related_name="caratteristicaprocedura",
        null=True,
        blank=True,
    )
    valore = models.CharField(max_length=100, null=True, blank=True)
    fk_lavorazione = models.ForeignKey(
        Lavorazione,
        on_delete=models.CASCADE,
        related_name="caratteristicaprocedura",
        null=True,
        blank=True,
    )
    note = models.TextField(null=True, blank=True)
    numero_riga = models.IntegerField()
    created_by = models.ForeignKey(
        User,
        related_name="caratteristicaprocedura",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)


class ElencoTest(models.Model):
    descrizione = models.CharField(max_length=100)
    norma_riferimento = models.CharField(max_length=100, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name="elenco_test",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.descrizione

    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "elenco test"


class TestArticolo(models.Model):

    # Interno/Esterno
    INTERNO = "interno"
    ESTERNO = "esterno"

    CHOICES_INT_EST = ((INTERNO, "Interno"), (ESTERNO, "Esterno"))

    fk_articolo = models.ForeignKey(
        Articolo, related_name="test_articolo", on_delete=models.CASCADE
    )
    fk_test = models.ForeignKey(
        ElencoTest, related_name="test_articolo", on_delete=models.CASCADE
    )
    valore = models.CharField(max_length=100, blank=True, null=True)
    interno_esterno = models.CharField(
        max_length=10, choices=CHOICES_INT_EST, null=True, blank=True
    )
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name="test_articolo",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)


class ListinoTerzista(models.Model):
    fk_fornitore = models.ForeignKey(Fornitore, on_delete=models.CASCADE)
    fk_lavorazione = models.ForeignKey(Lavorazione, on_delete=models.CASCADE)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name="listino_terzista",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def ultimo_prezzo(self):
        ultimo_prezzo = self.prezzo.order_by("-data_inserimento").first()
        if ultimo_prezzo:
            return ultimo_prezzo.prezzo
        return None


class PrezzoListino(models.Model):
    fk_listino_terzista = models.ForeignKey(
        ListinoTerzista, on_delete=models.CASCADE, related_name="prezzo"
    )
    data_inserimento = models.DateField(default=date.today)
    prezzo = models.DecimalField(max_digits=8, decimal_places=3)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name="prezzo_listino",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_inserimento"]

    def __str__(self):
        return f"Prezzo: {self.prezzo} - Data inserimento: {self.data_inserimento}"


class ListinoCliente(models.Model):
    fk_cliente = models.ForeignKey(
        Cliente, related_name="listino_cliente", on_delete=models.CASCADE
    )
    fk_articolo = models.ForeignKey(
        Articolo, related_name="listino_cliente", on_delete=models.CASCADE
    )
    prezzo = models.DecimalField(max_digits=8, decimal_places=3)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name="listino_cliente",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fk_articolo.descrizione
