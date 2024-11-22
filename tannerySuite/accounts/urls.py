from django.urls import path
from .views import registrazione_view, profile

urlpatterns = [
    path("registrazione/", registrazione_view, name="registrazione_view"),
    path("profile/", profile, name="profile"),
]