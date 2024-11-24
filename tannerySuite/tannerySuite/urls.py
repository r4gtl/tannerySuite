from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from core.views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('acquistopelli/', include('acquistopelli.urls')),
    path('anagrafiche/', include('anagrafiche.urls')),
    path('articoli/', include('articoli.urls')),
    path('lavorazioni/', include('lavorazioni.urls')),
    path('core/', include('core.urls')),
    path('nonconformity/', include('nonconformity.urls')),
]
