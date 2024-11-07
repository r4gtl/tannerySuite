from anagrafiche.models import Facility


def nome_sito(request):
    facility = Facility.objects.first()  # Scegli la Facility corretta o utilizza la logica di scelta desiderata
    return {'nome_sito': facility.nome_sito if facility else ''}

def logo_sito(request):
    facility = Facility.objects.first()  # Scegli la Facility corretta o utilizza la logica di scelta desiderata
    return {'logo_sito': facility.logo if facility else ''}

