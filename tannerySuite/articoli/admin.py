from django.contrib import admin

# Register your models here.

from .models import (Articolo, Colore, Lavorazione
                    )

admin.site.register(Articolo)
admin.site.register(Colore)
admin.site.register(Lavorazione)

