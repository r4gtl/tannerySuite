from datetime import date, datetime

# import datetime
from django.db import models
from django.contrib.auth.models import User
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


def get_current_time():
    return datetime.now().time()


class CausaleTrasporto(models.Model):
    """Utilizzare la PK come codice anche per la ricerca (vedi programma ddt)"""

    descrizione = models.CharField(max_length=50)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name="causali_trasporto",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "causali trasporto"

    def __str__(self):
        return self.descrizione


class AspettoDeiBeni(models.Model):
    """Utilizzare la PK come codice anche per la ricerca (vedi programma ddt)"""

    descrizione = models.CharField(max_length=50)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name="aspetto_beni",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "aspetto dei beni"

    def __str__(self):
        return self.descrizione


class PortoMateriale(models.Model):
    """Utilizzare la PK come codice anche per la ricerca (vedi programma ddt)"""

    descrizione = models.CharField(max_length=50)
    descrizione_inglese = models.CharField(max_length=50, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name="porto_materiale",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "aspetto dei beni"

    def __str__(self):
        return self.descrizione


class UnitaMisura(models.Model):
    """Utilizzare la PK come codice anche per la ricerca (vedi programma ddt)"""

    descrizione = models.CharField(max_length=50)
    abbreviazione = models.CharField(max_length=2)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name="unita_misura",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "unità di misura"

    def __str__(self):
        return self.abbreviazione


class OrdineLavoro(models.Model):

    INTERNO = "interno"
    ESTERNO = "esterno"

    CHOICES_INT_EST = ((INTERNO, "Interno"), (ESTERNO, "Esterno"))

    MITTENTE = "mittente"
    VETTORE = "vettore"
    DESTINATARIO = "destinatario"

    CHOICES_TRASPORTO = (
        (MITTENTE, "Mittente"),
        (VETTORE, "Vettore"),
        (DESTINATARIO, "Destinatario"),
    )
    int_est = models.CharField(max_length=10, choices=CHOICES_INT_EST, default=INTERNO)
    num_doc = models.IntegerField(default=None)
    data_doc = models.DateField(default=date.today)
    fk_fornitore = models.ForeignKey(
        Fornitore, related_name="ordine_lavoro", on_delete=models.CASCADE
    )
    fk_destinazione_diversa = models.ForeignKey(
        DestinazioneDiversaFornitore,
        null=True,
        blank=True,
        related_name="ordine_lavoro",
        on_delete=models.SET_NULL,
    )
    fk_causale_trasporto = models.ForeignKey(
        CausaleTrasporto, related_name="ordine_lavoro", on_delete=models.CASCADE
    )
    trasporto = models.CharField(
        max_length=20,
        choices=CHOICES_TRASPORTO,
        default=MITTENTE,
    )
    data_inizio_trasporto = models.DateField(default=date.today)
    ora_inizio_trasporto = models.TimeField(default=get_current_time)
    fk_vettore = models.ForeignKey(
        Fornitore,
        null=True,
        blank=True,
        related_name="ordine_lavoro_vettore",
        on_delete=models.SET_NULL,
    )
    n_colli = models.IntegerField(null=True, blank=True)
    fk_aspetto_beni = models.ForeignKey(
        AspettoDeiBeni, related_name="ordine_lavoro", on_delete=models.CASCADE
    )
    peso_kg = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name="ordine_lavoro",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)


class DettaglioOrdineLavoro(models.Model):
    numero_riga = models.IntegerField()
    fk_ordine_lavoro = models.ForeignKey(
        OrdineLavoro, related_name="dettaglio_ordine_lavoro", on_delete=models.CASCADE
    )
    fk_dettaglio_lotto = models.ForeignKey(
        DettaglioLotto,
        null=True,
        blank=True,
        related_name="dettaglio_ordine_lavoro",
        on_delete=models.SET_NULL,
    )
    fk_output_lavorazione = models.ForeignKey(
        "OutputLavorazione",
        null=True,
        blank=True,
        related_name="dettaglio_ordine_lavoro",
        on_delete=models.SET_NULL,
    )
    descrizione = models.CharField(max_length=100, null=True, blank=True)
    fk_lavorazione = models.ForeignKey(
        Lavorazione,
        null=True,
        blank=True,
        related_name="dettaglio_ordine_lavoro",
        on_delete=models.SET_NULL,
    )
    fk_unita_misura = models.ForeignKey(
        UnitaMisura,
        null=True,
        blank=True,
        related_name="dettaglio_ordine_lavoro",
        on_delete=models.SET_NULL,
    )
    quantity = models.IntegerField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name="dettaglio_ordine_lavoro",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["numero_riga"]


class OutputLavorazione(models.Model):

    CONSEGNA_FATT = "consegna fatturabile"
    CONSEGNA_NON_FATT = "consegna non fatturabile"
    RESTITUZIONE_FATT = "restituzione fatturabile"
    SCARTO_NON_FATT = "scarto non fatturabile"
    BOLLA_FATT_SUB_FOR = "bolla fattura subfornitore"

    CHOICES_CONSEGNA = (
        (CONSEGNA_FATT, "Consegna fatturabile"),
        (CONSEGNA_NON_FATT, "Consegna non fatturabile"),
        (RESTITUZIONE_FATT, "Restituzione fatturabile"),
        (SCARTO_NON_FATT, "Scarto non fatturabile"),
        (BOLLA_FATT_SUB_FOR, "Bolla fattura subfornitore"),
    )

    fk_dettaglio_ordine = models.ForeignKey(
        DettaglioOrdineLavoro,
        related_name="output_lavorazione",
        on_delete=models.CASCADE,
    )
    in_out = models.CharField(
        max_length=50,
        choices=CHOICES_CONSEGNA,
        default=CONSEGNA_FATT,
    )
    n_doc_reso = models.IntegerField(default=None)
    data_doc_reso = models.DateField()
    fk_dettaglio_lotto = models.ForeignKey(
        DettaglioLotto, related_name="output_lavorazione", on_delete=models.CASCADE
    )
    fk_fornitore_origine = models.ForeignKey(
        Fornitore, related_name="output_lavorazione", on_delete=models.CASCADE
    )
    fk_fornitore_destinatario = models.ForeignKey(
        Fornitore,
        null=True,
        blank=True,
        related_name="output_lavorazione_dest",
        on_delete=models.SET_NULL,
    )
    fk_lavorazione = models.ForeignKey(
        Lavorazione,
        null=True,
        blank=True,
        related_name="output_lavorazione",
        on_delete=models.SET_NULL,
    )
    fk_taglio = models.ForeignKey(
        Taglio,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="output_lavorazione",
    )
    fk_sezione = models.ForeignKey(
        Sezione,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="output_lavorazione",
    )
    fk_concia = models.ForeignKey(
        Concia,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="output_lavorazione",
    )
    fk_tipoanimale = models.ForeignKey(
        TipoAnimale,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="output_lavorazione",
    )
    fk_spessore = models.ForeignKey(
        Spessore,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="output_lavorazione",
    )
    fk_quality = models.ForeignKey(
        Quality,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="output_lavorazione",
    )
    quantity_output = models.IntegerField(null=True, blank=True)
    prezzo = models.DecimalField(max_digits=8, decimal_places=3)
    valore_output = models.DecimalField(max_digits=8, decimal_places=3)
    is_scarto = models.BooleanField(default=False)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name="output_lavorazione",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)
