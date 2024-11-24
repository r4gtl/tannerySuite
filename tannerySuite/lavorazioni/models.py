from django.db import models
from django.contrib.auth.models import User





class Lavorazione(models.Model):
    descrizione = models.CharField(max_length=50)
    codice = models.CharField(max_length=10, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='lavorazione', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["descrizione"]
        verbose_name_plural = "lavorazioni"

    def __str__(self):
        return self.descrizione
    

