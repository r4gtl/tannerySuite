from django.contrib import admin
from .models import (TipoAnimale,
                    TipoGrezzo,
                    Lotto,
                    Scelta,
                    )


admin.site.register(TipoAnimale)
admin.site.register(TipoGrezzo)
admin.site.register(Lotto)
admin.site.register(Scelta)