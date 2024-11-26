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
    
    

    context = {'causali_trasporto': causali_trasporto, 
                'aspetto_beni': aspetto_beni,  
                'porti_materiale': porti_materiale,
                
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
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('lavorazioni:tabelle_generiche')
        
        pk_fase=self.object.pk
        return reverse_lazy('lavorazioni:modifica_aspetto_beni', kwargs={'pk':pk_fase})
    
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
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('lavorazioni:tabelle_generiche')
        
        pk_fase=self.object.pk
        return reverse_lazy('lavorazioni:modifica_porto_materiale', kwargs={'pk':pk_fase})
    
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
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('lavorazioni:tabelle_generiche')
        
        pk_fase=self.object.pk
        return reverse_lazy('lavorazioni:modifica_porto_materiale', kwargs={'pk':pk_fase})
    
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

# Fine tabelle generiche

# Ordine di Lavoro    
class OrdineLavoroCreateView(LoginRequiredMixin,CreateView):
    model = OrdineLavoro
    form_class = OrdineLavoroModelForm
    template_name = 'lavorazioni/ordine_lavoro.html'
    success_message = 'DDT aggiunto correttamente!'
    success_url = reverse_lazy('lavorazioni:dashboard_lavorazioni')
  
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
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
    

def delete_ordine_lavoro(request, pk): 
        deleteobject = get_object_or_404(OrdineLavoro, pk = pk)          
        deleteobject.delete()
        url_match = reverse_lazy('lavorazioni:dashboard_lavorazioni')
        return redirect(url_match)