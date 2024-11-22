from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Sum


from .filters import LottoFilter

from .models import *

from .forms import *

from .utils import filtro_lotti



def dashboard_acquisto_pelli(request):     
    lotti = Lotto.objects.all()
    
    lotti_filter = LottoFilter(request.GET, queryset=lotti)
    
    page = request.GET.get('page', 1)
    paginator = Paginator(lotti_filter.qs, 50)  # Utilizza lotti_filter.qs per la paginazione
    
        
    try:
        lotti_paginator = paginator.page(page)
    except PageNotAnInteger:
        lotti_paginator = paginator.page(1)
    except EmptyPage:
        lotti_paginator = paginator.page(paginator.num_pages)
        
    context = {
        'lotti_paginator': lotti_paginator,
        'filter': lotti_filter,
    }
    
    return render(request, 'acquistopelli/dashboard_acquisto_pelli.html', context)


class LottoCreateView(LoginRequiredMixin,CreateView):
    model = Lotto
    form_class = LottoModelForm
    template_name = 'acquistopelli/lotto.html'
    success_message = 'Lotto aggiunto correttamente!'
    #success_url = reverse_lazy('human_resources:human_resources')

    def get_success_url(self):        
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('acquistopelli:dashboard_acquisto_pelli')
        
        pk_lotto=self.object.pk
        return reverse_lazy('acquistopelli:modifica_lotto', kwargs={'pk':pk_lotto})
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

class LottoUpdateView(LoginRequiredMixin, UpdateView):
    model = Lotto
    form_class = LottoModelForm
    template_name = 'acquistopelli/lotto.html'
    success_message = 'Lotto modificato correttamente!'
    #success_url = reverse_lazy('human_resources:tabelle_generiche_formazione')
    
    def get_success_url(self):        
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('acquistopelli:dashboard_acquisto_pelli')
        
        pk_lotto=self.object.pk
        return reverse_lazy('acquistopelli:modifica_lotto', kwargs={'pk':pk_lotto})
    

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        pk = self.object.pk   
        totale_pezzi = SceltaLotto.objects.filter(fk_lotto=pk).aggregate(Sum('pezzi'))['pezzi__sum'] or 0
        context['scelte_effettuate'] = SceltaLotto.objects.filter(fk_lotto=pk) 
        scelte_effettuate=SceltaLotto.objects.filter(fk_lotto=pk) 
        for scelta in scelte_effettuate:
            print(f"scelta {scelta.fk_scelta.pk}")
            print(f"scelta pezzi {scelta.pezzi}")
            print(f"scelta pk {scelta.pk}")
        context['totale_pezzi'] = totale_pezzi
        lotto = Lotto.objects.get(pk=pk)
        pezzi_rimanenti = lotto.pezzi - totale_pezzi
        context['pezzi_rimanenti'] = pezzi_rimanenti
        return context



# Dettaglio scelta lotto
class SceltaLottoCreateView(LoginRequiredMixin, CreateView):
    model = SceltaLotto
    form_class = SceltaLottoModelForm
    template_name = 'acquistopelli/scelta_lotto.html'
    success_message = 'Dettaglio aggiunto correttamente!'
    
    def get_initial(self):        
        fk_lotto = self.kwargs['pk'] 
        print("Lotto initial:" + str(fk_lotto))
        created_by = self.request.user       
        return {
            'fk_lotto': fk_lotto,
            'created_by': created_by
        }

    def get_success_url(self):          
        fk_lotto=self.object.fk_lotto.pk   
        print("fkLotto: " + str(fk_lotto))     
        return reverse_lazy('acquistopelli:modifica_lotto', kwargs={'pk':fk_lotto})
    
    def form_valid(self, form):                
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']       
        context['fk_lotto'] = Lotto.objects.get(pk=pk) 
        return context
    
    
class SceltaLottoUpdateView(LoginRequiredMixin, UpdateView):
    model = SceltaLotto
    form_class = SceltaLottoModelForm
    template_name = 'acquistopelli/scelta_lotto.html'
    success_message = 'Dettaglio modificato correttamente!'
    #success_url = reverse_lazy('human_resources:crea_registro_formazione', kwargs={"pk": pk})
    
    def get_success_url(self):          
        fk_lotto=self.object.fk_lotto.pk        
        return reverse_lazy('acquistopelli:modifica_lotto', kwargs={'pk':fk_lotto})
    
    def form_valid(self, form):                
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']       
        context['fk_lotto'] = Lotto.objects.get(pk=pk)
        return context
    


def delete_scelta_lotto(request, pk): 
        deleteobject = get_object_or_404(SceltaLotto, pk = pk)   
        fk_lotto = deleteobject.fk_lotto.pk      
        deleteobject.delete()
        url_match = reverse_lazy('acquistopelli:modifica_lotto', kwargs={'pk':fk_lotto})
        return redirect(url_match)


'''SEZIONE TABELLE GENERICHE'''

def tabelle_generiche_acquisto_pelli(request):
    tipianimale = TipoAnimale.objects.all()
    tipigrezzo = TipoGrezzo.objects.all()
    scelte = Scelta.objects.all()
    

    context = {'tipianimale': tipianimale, 
                'tipigrezzo': tipigrezzo,  
                'scelte': scelte              
                }
    
    return render(request, "acquistopelli/tabelle_generiche_acquisto_pelli.html", context)


class TipoAnimaleCreateView(LoginRequiredMixin,CreateView):
    model = TipoAnimale
    form_class = TipoAnimaleModelForm
    template_name = 'acquistopelli/tipo_animale.html'
    success_message = 'Tipo Animale aggiunto correttamente!'
    success_url = reverse_lazy('acquistopelli:tabelle_generiche_acquisto_pelli')
  
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }
    
class TipoAnimaleUpdateView(LoginRequiredMixin,UpdateView):
    model = TipoAnimale
    form_class = TipoAnimaleModelForm
    template_name = 'acquistopelli/tipo_animale.html'
    success_message = 'Tipo Animale modificato correttamente!'
    success_url = reverse_lazy('acquistopelli:tabelle_generiche_acquisto_pelli')

    
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    

def delete_tipo_animale(request, pk): 
        deleteobject = get_object_or_404(TipoAnimale, pk = pk)          
        deleteobject.delete()
        url_match= reverse_lazy('acquistopelli:tabelle_generiche_acquisto_pelli')
        return redirect(url_match)


class TipoGrezzoCreateView(LoginRequiredMixin,CreateView):
    model = TipoGrezzo
    form_class = TipoGrezzoModelForm
    template_name = 'acquistopelli/tipo_grezzo.html'
    success_message = 'Tipo Grezzo aggiunto correttamente!'
    success_url = reverse_lazy('acquistopelli:tabelle_generiche_acquisto_pelli')

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }
    
class TipoGrezzoUpdateView(LoginRequiredMixin,UpdateView):
    model = TipoGrezzo
    form_class = TipoGrezzoModelForm
    template_name = 'acquistopelli/tipo_grezzo.html'
    success_message = 'Tipo Grezzo modificato correttamente!'
    success_url = reverse_lazy('acquistopelli:tabelle_generiche_acquisto_pelli')

    
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    

def delete_tipo_grezzo(request, pk): 
        deleteobject = get_object_or_404(TipoGrezzo, pk = pk)          
        deleteobject.delete()
        url_match= reverse_lazy('acquistopelli:tabelle_generiche_acquisto_pelli')
        return redirect(url_match)


class SceltaCreateView(LoginRequiredMixin,CreateView):
    model = Scelta
    form_class = SceltaModelForm
    template_name = 'acquistopelli/scelta.html'
    success_message = 'Scelta aggiunta correttamente!'
    success_url = reverse_lazy('acquistopelli:tabelle_generiche_acquisto_pelli')
   
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }
    

class SceltaUpdateView(LoginRequiredMixin,UpdateView):
    model = Scelta
    form_class = SceltaModelForm
    template_name = 'acquistopelli/scelta.html'
    success_message = 'Scelta modificata correttamente!'
    success_url = reverse_lazy('acquistopelli:tabelle_generiche_acquisto_pelli')

    
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    

def delete_scelta(request, pk): 
        deleteobject = get_object_or_404(Scelta, pk = pk)          
        deleteobject.delete()
        url_match= reverse_lazy('acquistopelli:tabelle_generiche_acquisto_pelli')
        return redirect(url_match)


'''FINE SEZIONE TABELLE GENERICHE'''

def report_traceability_in(request):
    if request.method == 'GET':
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')

        
        from_date_formatted = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date_formatted = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()

        lotti_filtrati= filtro_lotti(from_date, to_date) 
        context = {
            'lotti_filtrati': lotti_filtrati,
            'from_date': from_date_formatted,
            'to_date': to_date_formatted
        }

        return render(request, 'acquistopelli/reports/report_traceability_in.html', context)
    else:
        # Gestisci eventuali altri metodi HTTP
        pass

                   