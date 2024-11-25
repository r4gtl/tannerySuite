from django.test import TestCase

from django.test import TestCase
from django.urls import reverse
from anagrafiche.models import Fornitore

class HomeFornitoriViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Fornitore.objects.bulk_create(
            [Fornitore(ragionesociale=f"Fornitore {i}", categoria="pelli" if i % 2 == 0 else "servizi") for i in range(1, 101)]
        )
        #[Fornitore.objects.create(ragionesociale="Fornitore Servizi", categoria="servizi") for i in range(1, 51)]
        
        # Salva l'URL
        cls.url = reverse('anagrafiche:home_fornitori')
            
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/anagrafiche/home_fornitori/')
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        response = self.client.get(reverse('anagrafiche:home_fornitori'))  # Assumi che il nome dell'URL sia `home_fornitori`
        self.assertEqual(response.status_code, 200)
        
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('anagrafiche:home_fornitori'))
        self.assertTemplateUsed(response, 'anagrafiche/home_fornitori.html')

    def test_context_contains_fornitori(self):
        response = self.client.get(reverse('anagrafiche:home_fornitori'))
        self.assertIn('fornitori_paginator', response.context)
        self.assertIn('filter', response.context)
        self.assertIn('CHOICES_CATEGORY', response.context)
        
    def test_pagination_is_fifty(self):
        # Ottieni la prima pagina della risposta
        response = self.client.get(self.url + '?categoria=pelli')  # Usa il filtro per 'pelli'
        
        # Verifica che ci siano 50 fornitori nella prima pagina
        self.assertEqual(len(response.context['fornitori_paginator']), 50)

    def test_pagination_second_page(self):
        # Ottieni la seconda pagina della risposta
        response = self.client.get(self.url + '?categoria=pelli&page=2')  # Usa il filtro per 'pelli'
        
        # Verifica che ci siano 50 fornitori nella seconda pagina
        self.assertEqual(len(response.context['fornitori_paginator']), 50)

    def test_filter_category_pelli(self):
        response = self.client.get(self.url + '?categoria=pelli')
        filtered_fornitori = response.context['filter'].qs
        
        # Assicurati che ci siano fornitori con la categoria 'pelli'
        self.assertEqual(filtered_fornitori.count(), 50, "Il filtro non ha restituito 50 fornitori con la categoria 'pelli'.")
        
        # Verifica che tutti i fornitori abbiano la categoria 'pelli'
        for f in filtered_fornitori:
            self.assertEqual(f.categoria, 'pelli', f"Fornitore {f.ragionesociale} ha una categoria diversa: {f.categoria}")
        
    def test_page_out_of_range(self):
        response = self.client.get(reverse('anagrafiche:home_fornitori') + '?page=100')
        self.assertEqual(response.context['fornitori_paginator'].number, response.context['fornitori_paginator'].paginator.num_pages)

    def test_choices_category_in_context(self):
        response = self.client.get(reverse('anagrafiche:home_fornitori'))
        self.assertEqual(response.context['CHOICES_CATEGORY'], Fornitore.CHOICES_CATEGORY)




