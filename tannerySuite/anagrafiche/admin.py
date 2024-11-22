from django.contrib import admin

# Register your models here.

from .models import (Fornitore, Facility,
                      FacilityContact, Cliente,
                        LwgFornitore, TransferValue,
                        FornitoreServizi, FornitoreLavorazioniEsterne, FornitorePelli, FornitoreProdottiChimici
                        )

admin.site.register(Fornitore)
admin.site.register(Facility)
admin.site.register(FacilityContact)
admin.site.register(Cliente)
admin.site.register(LwgFornitore)
admin.site.register(TransferValue)
admin.site.register(FornitoreServizi)
admin.site.register(FornitoreLavorazioniEsterne)
admin.site.register(FornitorePelli)
admin.site.register(FornitoreProdottiChimici)