from datetime import date
#import datetime
from django.db import models
from django.contrib.auth.models import User
from anagrafiche.models import Fornitore



class CausaleTrasporto(models.Model):
    '''Utilizzare la PK come codice anche per la ricerca (vedi programma ddt)'''
    descrizione = models.CharField(max_length=50)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='causali_trasporto', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "causali trasporto"

    def __str__(self):
        return self.descrizione
    

class AspettoDeiBeni(models.Model):
    '''Utilizzare la PK come codice anche per la ricerca (vedi programma ddt)'''
    descrizione = models.CharField(max_length=50)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='aspetto_beni', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "aspetto dei beni"

    def __str__(self):
        return self.descrizione
    
class PortoMateriale(models.Model):
    '''Utilizzare la PK come codice anche per la ricerca (vedi programma ddt)'''
    descrizione = models.CharField(max_length=50)
    decrizione_inglese = models.CharField(max_length=50)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='porto_materiale', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "aspetto dei beni"

    def __str__(self):
        return self.descrizione
    
class OrdineLavoro(models.Model):
    
    INTERNO = 'interno'
    ESTERNO = 'esterno'
    
    CHOICES_INT_EST = (
        (INTERNO, 'Interno'),
        (ESTERNO, 'Esterno')
        
    )
    
    MITTENTE = 'mittente'
    VETTORE = 'vettore'
    DESTINATARIO = 'destinatario'

    CHOICES_TRASPORTO = (
        (MITTENTE, 'Mittente'),
        (VETTORE, 'Vettore'),
        (DESTINATARIO, 'Destinatario'),
    )

    
    
    int_est = models.CharField(max_length=10, choices=CHOICES_INT_EST, default=INTERNO)
    num_doc = models.IntegerField(default=None)
    data_doc = models.DateField(default=date.today)
    fk_fornitore = models.ForeignKey(Fornitore, related_name='ordine_lavoro', on_delete=models.CASCADE)
    fk_causale_trasporto = models.ForeignKey(CausaleTrasporto, related_name='ordine_lavoro', on_delete=models.CASCADE)
    trasporto = models.CharField(
        max_length=20,
        choices=CHOICES_TRASPORTO,
        default=MITTENTE,
    )
    #data_inizio_trasporto = models.DateField(default=datetime.date.today)
    #ora_inizio_trasporto = models.TimeField(default=datetime.datetime.now().time)    
    n_colli = models.IntegerField(null=True, blank=True)
    peso_kg = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, )
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='ordine_lavoro', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    
    