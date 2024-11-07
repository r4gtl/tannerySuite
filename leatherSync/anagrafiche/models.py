from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django_countries.fields import \
    CountryField  # Field from django countries app


class Facility(models.Model):
    #
    # Categorie produzione
    CAT0 = 'Nessuna categoria'
    CAT1 = 'A - Raw hide/skin to tanned'
    CAT2 = 'B - Raw hide/skin to crust'
    CAT3 = 'C - Raw hide/skin to finished leather'
    CAT4 = 'D - Tanned hide/skin to finished leather'
    CAT5 = 'E - Crust hide/skin to finished leather'
    CAT6 = 'F - Tanned hide/skin to crust leather'
    CAT7 = 'G - Raw hide/skin to pickled/pre-tanned material'
    
    
    CHOICES_PRODUCTION_CATEGORY = (
        (CAT0, 'Nessuna categoria'),
        (CAT1, 'A - Raw hide/skin to tanned'),
        (CAT2, 'B - Raw hide/skin to crust'),
        (CAT3, 'C - Raw hide/skin to finished leather'),
        (CAT4, 'D - Tanned hide/skin to finished leather'),
        (CAT5, 'E - Crust hide/skin to finished leather'),
        (CAT6, 'F - Tanned hide/skin to crust leather'),
        (CAT7, 'G - Raw hide/skin to pickled/pre-tanned material'),        
    )
    
    nome_sito = models.CharField(max_length=100)
    logo = models.ImageField(default='avatar.png', upload_to='logo')
    urn = models.CharField(max_length=50, blank=True, null=True)
    piva = models.CharField(max_length=11, blank=True, null=True)
    indirizzo = models.CharField(max_length=100, blank=True, null=True)
    cap = models.CharField(max_length=5, blank=True, null=True)
    city = models.CharField(max_length=100,blank=True, null=True)
    provincia = models.CharField(max_length=2, blank=True, null=True)
    country = CountryField(blank_label='(seleziona Paese)')
    phone = models.CharField(max_length=50, blank=True, null=True)
    primary_cat = models.CharField(max_length=50, choices=CHOICES_PRODUCTION_CATEGORY, default=CAT0)
    secondary_cat = models.CharField(max_length=50, choices=CHOICES_PRODUCTION_CATEGORY, default=CAT0)
    tertiary_cat = models.CharField(max_length=50, choices=CHOICES_PRODUCTION_CATEGORY, default=CAT0)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)    
    site_area = models.FloatField(blank=True, null=True)
    facility_description= models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nome_sito
    
    def get_absolute_url(self):
        return reverse("anagrafiche:edit_facility_details", kwargs={"pk": self.pk})
    
class FacilityContact(models.Model):
    #
    # Tipo Contatti
    CONT_1 = '6a - Principal Contact Name and position'
    CONT_2 = '6b - Ultimately responsible for environmental issue at this site'
    CONT_3 = '6c - Responsible on a day-to-day basis for environmental issue at this site'
    CONT_4 = '7 - Others'
    
    CHOICES_CONTACT_TYPE = (
        (CONT_1, '6a - Principal Contact Name and position'),
        (CONT_2, '6b - Ultimately responsible for environmental issue at this site'),
        (CONT_3, '6c - Responsible on a day-to-day basis for environmental issue at this site'),
        (CONT_4, '7 - Others')
    )
    
    fk_facility = models.ForeignKey(Facility, related_name='contacts', on_delete=models.CASCADE)
    contact_type = models.CharField(max_length=100, choices=CHOICES_CONTACT_TYPE, default=CONT_4)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    

