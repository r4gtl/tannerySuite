from django.core.management.base import BaseCommand
from faker import Faker
from anagrafiche.models import Fornitore
from django_countries import countries
import random

fake = Faker('it_IT')

class Command(BaseCommand):
    help = 'Popola il database con dati dummy'

    def handle(self, *args, **kwargs):
        self.stdout.write("Inizio popolamento database...")

        # Estrai la lista dei codici dei paesi disponibili in django-countries
        lista_paesi = [code for code, name in countries]
        
        categorie = [choice[0] for choice in Fornitore.CHOICES_CATEGORY]
        
        # Popola il database
        for _ in range(500):  
            Fornitore.objects.create(
                ragionesociale=fake.company(),
                indirizzo=fake.street_address(),
                cap=fake.postcode(),
                city=fake.city(),
                provincia=fake.state(),
                country=fake.random_element(lista_paesi),
                sito_web=fake.url(),
                e_mail=fake.email(),
                categoria=random.choice(categorie),
                created_by=None,
                
            )
        
        self.stdout.write(self.style.SUCCESS("Popolamento completato!"))
