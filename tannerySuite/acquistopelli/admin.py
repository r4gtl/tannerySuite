from django.contrib import admin
from .models import (TipoAnimale,
                     TipoGrezzo,
                     Lotto,
                     Scelta,
                     )
# Register your models here.

admin.site.register(TipoAnimale)
admin.site.register(TipoGrezzo)
admin.site.register(Lotto)
admin.site.register(Scelta)