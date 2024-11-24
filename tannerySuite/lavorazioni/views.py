import datetime
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView


from .models import *

from .forms import *

from .filters import LavorazioneFilter


def dashboard_lavorazioni(request):     
    lavorazioni = Lavorazione.objects.all()
    
    lavorazioni_filter = LavorazioneFilter(request.GET, queryset=lavorazioni)
    
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


class LavorazioneCreateView(LoginRequiredMixin,CreateView):
    model = Lavorazione
    form_class = LavorazioneModelForm
    template_name = 'lavorazioni/lavorazione.html'
    success_message = 'Lavorazione aggiunta correttamente!'
    success_url = reverse_lazy('lavorazioni:dashboard_lavorazioni')
  
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }
    
class LavorazioneUpdateView(LoginRequiredMixin,UpdateView):
    model = Lavorazione
    form_class = LavorazioneModelForm
    template_name = 'lavorazioni/lavorazione.html'
    success_message = 'Lavorazione modificata correttamente!'
    success_url = reverse_lazy('lavorazioni:dashboard_lavorazioni')

    
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    

def delete_lavorazione(request, pk): 
        deleteobject = get_object_or_404(Lavorazione, pk = pk)          
        deleteobject.delete()
        url_match = reverse_lazy('lavorazioni:dashboard_lavorazioni')
        return redirect(url_match)