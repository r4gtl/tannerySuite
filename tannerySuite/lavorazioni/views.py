import datetime
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView


from .models import *

from .forms import *

from .filters import OrdineLavoroFilter


def dashboard_lavorazioni(request):     
    lavorazioni = OrdineLavoro.objects.all()
    
    lavorazioni_filter = OrdineLavoroFilter(request.GET, queryset=lavorazioni)
    
    page = request.GET.get('page', 1)
    paginator = Paginator(lavorazioni_filter.qs, 50)  # Utilizza lotti_filter.qs per la paginazione
    
        
    try:
        lavorazioni_paginator = paginator.page(page)
    except PageNotAnInteger:
        lavorazioni_paginator = paginator.page(1)
    except EmptyPage:
        lavorazioni_paginator = paginator.page(paginator.num_pages)
        
    context = {
        'lavorazioni_paginator': lavorazioni_paginator,
        'filter': lavorazioni_filter,
    }
    
    return render(request, 'lavorazioni/dashboard_lavorazioni.html', context)

# Tabelle Generiche

def tabelle_generiche(request):
    causali_trasporto = CausaleTrasporto.objects.all()
    aspetto_beni = AspettoDeiBeni.objects.all()
    porti_materiale = PortoMateriale.objects.all()
    uni_misura = UnitaMisura.objects.all()
    
    

    context = {'causali_trasporto': causali_trasporto, 
                'aspetto_beni': aspetto_beni,  
                'porti_materiale': porti_materiale,
                'uni_misura': uni_misura
                
                }
    
    return render(request, "lavorazioni/tabelle_generiche.html", context)
class CausaleTrasportoCreateView(LoginRequiredMixin,CreateView):
    model = CausaleTrasporto
    form_class = CausaleTrasportoModelForm
    template_name = 'lavorazioni/generiche/causale_trasporto.html'
    success_message = 'Causale di trasporto aggiunta correttamente!'
    #success_url = reverse_lazy('human_resources:human_resources')

    def get_success_url(self):        
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('lavorazioni:tabelle_generiche')
        
        pk_fase=self.object.pk
        return reverse_lazy('lavorazioni:modifica_causale_trasporto', kwargs={'pk':pk_fase})
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    

class CausaleTrasportoUpdateView(LoginRequiredMixin,UpdateView):
    model = CausaleTrasporto
    form_class = CausaleTrasportoModelForm
    template_name = 'lavorazioni/generiche/causale_trasporto.html'
    success_message = 'Causale di trasporto modificata correttamente!'
    #success_url = reverse_lazy('human_resources:human_resources')

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_success_url(self):        
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('lavorazioni:tabelle_generiche')
        
        pk_fase=self.object.pk
        return reverse_lazy('lavorazioni:modifica_causale_trasporto', kwargs={'pk':pk_fase})
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        # context['elenco_attributi'] = DettaglioFaseLavoro.objects.filter(fk_fase_lavoro=self.object.pk)
        # context['elenco_valutazioni'] = ValutazioneOperatore.objects.filter(fk_hr=self.object.pk)
        return context
    
def delete_causale_trasporto(request, pk): 
        deleteobject = get_object_or_404(CausaleTrasporto, pk = pk)        
        deleteobject.delete()
        url_match= reverse_lazy('lavorazioni:tabelle_generiche')
        return redirect(url_match)
    

class AspettoDeiBeniCreateView(LoginRequiredMixin,CreateView):
    model = AspettoDeiBeni
    form_class = AspettoDeiBeniModelForm
    template_name = 'lavorazioni/generiche/aspetto_beni.html'
    success_message = 'Aspetto dei beni aggiunto correttamente!'
    #success_url = reverse_lazy('human_resources:human_resources')

    def get_success_url(self):        
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('lavorazioni:tabelle_generiche')
        
        pk_fase=self.object.pk
        return reverse_lazy('lavorazioni:modifica_aspetto_beni', kwargs={'pk':pk_fase})
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    

class AspettoDeiBeniUpdateView(LoginRequiredMixin,UpdateView):
    model = AspettoDeiBeni
    form_class = AspettoDeiBeniModelForm
    template_name = 'lavorazioni/generiche/aspetto_beni.html'
    success_message = 'Aspetto beni modificato correttamente!'
    #success_url = reverse_lazy('human_resources:human_resources')

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_success_url(self): 
        return reverse_lazy('lavorazioni:tabelle_generiche')
        
        
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        # context['elenco_attributi'] = DettaglioFaseLavoro.objects.filter(fk_fase_lavoro=self.object.pk)
        # context['elenco_valutazioni'] = ValutazioneOperatore.objects.filter(fk_hr=self.object.pk)
        return context
    
def delete_aspetto_beni(request, pk): 
        deleteobject = get_object_or_404(AspettoDeiBeni, pk = pk)        
        deleteobject.delete()
        url_match= reverse_lazy('lavorazioni:tabelle_generiche')
        return redirect(url_match)
        

class PortoMaterialeCreateView(LoginRequiredMixin,CreateView):
    model = PortoMateriale
    form_class = PortoMaterialeModelForm
    template_name = 'lavorazioni/generiche/porto_materiale.html'
    success_message = 'Porto materiale aggiunto correttamente!'
    #success_url = reverse_lazy('human_resources:human_resources')

    def get_success_url(self):                
        return reverse_lazy('lavorazioni:tabelle_generiche')
        
        
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    

class PortoMaterialeUpdateView(LoginRequiredMixin,UpdateView):
    model = PortoMateriale
    form_class = PortoMaterialeModelForm
    template_name = 'lavorazioni/generiche/porto_materiale.html'
    success_message = 'Porto materiale modificato correttamente!'
    #success_url = reverse_lazy('human_resources:human_resources')

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_success_url(self): 
        return reverse_lazy('lavorazioni:tabelle_generiche')
        
        
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        # context['elenco_attributi'] = DettaglioFaseLavoro.objects.filter(fk_fase_lavoro=self.object.pk)
        # context['elenco_valutazioni'] = ValutazioneOperatore.objects.filter(fk_hr=self.object.pk)
        return context
    
def delete_porto_materiale(request, pk): 
        deleteobject = get_object_or_404(PortoMateriale, pk = pk)        
        deleteobject.delete()
        url_match= reverse_lazy('lavorazioni:tabelle_generiche')
        return redirect(url_match)


class UnitaMisuraCreateView(LoginRequiredMixin,CreateView):
    model = UnitaMisura
    form_class = UnitaMisuraModelForm
    template_name = 'lavorazioni/generiche/unita_misura.html'
    success_message = 'Unità di misura aggiunta correttamente!'
    #success_url = reverse_lazy('human_resources:human_resources')

    def get_success_url(self):                
        return reverse_lazy('lavorazioni:tabelle_generiche')
        
        
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    

class UnitaMisuraUpdateView(LoginRequiredMixin,UpdateView):
    model = UnitaMisura
    form_class = UnitaMisuraModelForm
    template_name = 'lavorazioni/generiche/unita_misura.html'
    success_message = 'Unità di misura modificata correttamente!'
    #success_url = reverse_lazy('human_resources:human_resources')

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_success_url(self): 
        return reverse_lazy('lavorazioni:tabelle_generiche')
        
        
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        
        # context['elenco_valutazioni'] = ValutazioneOperatore.objects.filter(fk_hr=self.object.pk)
        return context
    
def delete_unita_misura(request, pk): 
        deleteobject = get_object_or_404(UnitaMisura, pk = pk)        
        deleteobject.delete()
        url_match= reverse_lazy('lavorazioni:tabelle_generiche')
        return redirect(url_match)
    
# Fine tabelle generiche

# Ordine di Lavoro    
class OrdineLavoroCreateView(LoginRequiredMixin,CreateView):
    model = OrdineLavoro
    form_class = OrdineLavoroModelForm
    template_name = 'lavorazioni/ordine_lavoro.html'
    success_message = 'DDT aggiunto correttamente!'
    #success_url = reverse_lazy('lavorazioni:dashboard_lavorazioni')
  
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_success_url(self):        
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('lavorazioni:dashboard_lavorazioni')
        
        pk_ordine_lavoro=self.object.pk
        return reverse_lazy('lavorazioni:crea_ordine_lavoro', kwargs={'pk':pk_ordine_lavoro})

        
    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }
    
class OrdineLavoroUpdateView(LoginRequiredMixin,UpdateView):
    model = OrdineLavoro
    form_class = OrdineLavoroModelForm
    template_name = 'lavorazioni/ordine_lavoro.html'
    success_message = 'Ordine lavoro modificato correttamente!'
    success_url = reverse_lazy('lavorazioni:dashboard_lavorazioni')

    
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    
    def get_success_url(self):        
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('lavorazioni:dashboard_lavorazioni')
        
        pk_ordine_lavoro=self.object.pk
        return reverse_lazy('lavorazioni:crea_ordine_lavoro', kwargs={'pk':pk_ordine_lavoro})
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        
        context['elenco_dettagli'] = DettaglioOrdineLavoro.objects.filter(fk_hr=self.object.pk)
        return context
    

def delete_ordine_lavoro(request, pk): 
        deleteobject = get_object_or_404(OrdineLavoro, pk = pk)          
        deleteobject.delete()
        url_match = reverse_lazy('lavorazioni:dashboard_lavorazioni')
        return redirect(url_match)
    
# Dettaglio
class DettaglioOrdineLavoroCreateView(LoginRequiredMixin,CreateView):
    model = DettaglioOrdineLavoro
    form_class = DettaglioOrdineLavoroModelForm
    template_name = 'ricette/dettaglio_ordine_lavoro.html'
    success_message = 'Dettaglio aggiunto correttamente!'


    def get_success_url(self):
        fk_ordine_lavoro=self.object.fk_ordine_lavoro.pk   
        #focus_button = 'btn_new_detail'  # Imposto il pulsante su cui settare il focus
        
        #return reverse_lazy('ricette:modifica_dettaglio_ricetta_rifinizione_with_focus_button', kwargs={'pk':fk_ricetta_rifinizione, 'focus_button': focus_button})     
        return reverse_lazy('lavorazioni:modifica_dettaglio_ordine_lavoro', kwargs={'pk':fk_ordine_lavoro})
    
      
    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    

    def get_initial(self):
        initial = super().get_initial()        
        ordine_lavoro_id = self.kwargs.get('fk_ordine_lavoro')
        max_numero_riga = DettaglioOrdineLavoro.objects.filter(fk_ordine_lavoro=ordine_lavoro_id).aggregate(models.Max('numero_riga'))['numero_riga__max']
        next_numero_riga = max_numero_riga + 1 if max_numero_riga else 1
        initial['numero_riga'] = next_numero_riga

        ordine_lavoro_id = self.kwargs.get('fk_ordine_lavoro')
        
        initial['fk_ordine_lavoro'] = ordine_lavoro_id
        initial['created_by'] = self.request.user        
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_ordine_lavoro = self.kwargs['fk_rordine_lavoro']         
        context['ordine_lavoro'] = pk_ordine_lavoro
        context['dettagli_ordine_lavoro'] = get_object_or_404(OrdineLavoro, pk=pk_ordine_lavoro)
        return context
        

class DettaglioOrdineLavoroUpdateView(LoginRequiredMixin, UpdateView):
    model = DettaglioOrdineLavoro
    form_class = DettaglioOrdineLavoroModelForm
    template_name = 'lavorazioni/dettaglio_ordine_lavoro.html'
    success_message = 'Dettaglio modificato correttamente!'


    def get_success_url(self):
        fk_ordine_lavoro=self.object.fk_ordine_lavoro.pk        
        return reverse_lazy('lavorazioni:modifica_dettaglio_ordine_lavoro', kwargs={'pk':fk_ordine_lavoro})
    


    def form_valid(self, form):
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_ordine_lavoro = self.kwargs['fk_ordine_lavoro']         
        context['ordine_lavoro'] = pk_ordine_lavoro
        context['dettagli_ordine_lavoro'] = get_object_or_404(OrdineLavoro, pk=pk_ordine_lavoro)
        return context


def delete_dettaglio_ordine_lavoro(request, pk):
        deleteobject = get_object_or_404(DettaglioOrdineLavoro, pk = pk)
        fk_ordine_lavoro = deleteobject.fk_ordine_lavoro.pk
        deleteobject.delete()
        url_match = reverse_lazy('lavorazioni:modifica_ordine_lavoro', kwargs={'pk':fk_ordine_lavoro})
        return redirect(url_match)