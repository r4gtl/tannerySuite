from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView



from .models import *
from .forms import *
from .filters import *


def home_rapporti_nc(request): 
    rapporti_nc = RapportoNC.objects.all()
    rapporti_nc_filter = RapportoNCFilter(request.GET, queryset=rapporti_nc)    
    page = request.GET.get('page', 1)
    paginator = Paginator(rapporti_nc_filter.qs, 50)  # Utilizza rapporti_nc_filter.qs per la paginazione
            
    try:
        rapporti_nc_filter_paginator = paginator.page(page)
    except PageNotAnInteger:
        rapporti_nc_filter_paginator = paginator.page(1)
    except EmptyPage:
        rapporti_nc_filter_paginator = paginator.page(paginator.num_pages)
        
    context = {
        
        'rapporti_nc_filter_paginator': rapporti_nc_filter_paginator,
        'filter': rapporti_nc_filter
    }
    return render(request, 'nonconformity/home_rapporti_nc.html', context)



class RapportoNCCreateView(LoginRequiredMixin,CreateView):
    model = RapportoNC
    form_class = RapportoNCModelForm
    template_name = 'nonconformity/rapporto_nc.html'
    success_message = 'Rapporto aggiunto correttamente!'
    

    def get_success_url(self):        
        
        return reverse_lazy('nonconformity:home_rapporti_nc')
        
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

class RapportoNCUpdateView(LoginRequiredMixin, UpdateView):
    model = RapportoNC
    form_class = RapportoNCModelForm
    template_name = 'nonconformity/rapporto_nc.html'
    success_message = 'Rapporto modificato correttamente!'
    
    
    def get_success_url(self):        
        
        return reverse_lazy('nonconformity:home_rapporti_nc')
            

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        # pk_procedura = self.object.pk        
        # context['elenco_revisioni'] = RevisioneProcedura.objects.filter(fk_procedura=pk_procedura) 
        # context['elenco_moduli'] = Modulo.objects.filter(fk_procedura=pk_procedura) 

        return context



def delete_rapporto_nc(request, pk): 
        deleteobject = get_object_or_404(RapportoNC, pk = pk)                 
        deleteobject.delete()
        url_match = reverse_lazy('nonconformity:home_rapporti_nc')
        return redirect(url_match)



'''Rapporti di Audit'''


def home_rapporti_audit(request): 
    rapporti_audit = RapportoAudit.objects.all()
    rapporti_audit_filter = RapportoAuditFilter(request.GET, queryset=rapporti_audit)
    #filterset_class = FornitoreFilter
    page = request.GET.get('page', 1)
    paginator = Paginator(rapporti_audit_filter.qs, 50)  # Utilizza rapporti_audit_filter.qs per la paginazione
            
    try:
        rapporti_audit_filter_paginator = paginator.page(page)
    except PageNotAnInteger:
        rapporti_audit_filter_paginator = paginator.page(1)
    except EmptyPage:
        rapporti_audit_filter_paginator = paginator.page(paginator.num_pages)
        
    context = {
        
        'rapporti_audit_filter_paginator': rapporti_audit_filter_paginator,
        'filter': rapporti_audit_filter
    }
    return render(request, 'nonconformity/home_rapporti_audit.html', context)



class RapportoAuditCreateView(LoginRequiredMixin,CreateView):
    model = RapportoAudit
    form_class = RapportoAuditModelForm
    template_name = 'nonconformity/rapporto_audit.html'
    success_message = 'Rapporto aggiunto correttamente!'
    



    def get_success_url(self):        
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('nonconformity:home_rapporti_audit')

        pk=self.object.pk
        return reverse_lazy('nonconformity:modifica_rapporto_audit', kwargs={'pk':pk})
        
        
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

class RapportoAuditUpdateView(LoginRequiredMixin, UpdateView):
    model = RapportoAudit
    form_class = RapportoAuditModelForm
    template_name = 'nonconformity/rapporto_audit.html'
    success_message = 'Rapporto modificato correttamente!'
    
    
    def get_success_url(self):    
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('nonconformity:home_rapporti_audit')

        pk=self.object.pk
        return reverse_lazy('nonconformity:modifica_rapporto_audit', kwargs={'pk':pk})
            

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        pk_rapporto = self.object.pk    
        
        context['nc_associate'] = RapportoNC.objects.filter(fk_rapportoaudit=pk_rapporto) 
        context['processi_audit'] = ProcessoAudit.objects.filter(fk_rapportoaudit=pk_rapporto) 

        return context



def delete_rapporto_audit(request, pk): 
        deleteobject = get_object_or_404(RapportoAudit, pk = pk)                 
        deleteobject.delete()
        url_match = reverse_lazy('nonconformity:home_rapporti_audit')
        return redirect(url_match)

'''TABELLE GENERICHE'''
def tabelle_generiche(request):
    processi = Processo.objects.all() 

    context = {'processi': processi, 
               
                }
    
    return render(request, "nonconformity/tabelle_generiche.html", context)



class ProcessoCreateView(LoginRequiredMixin,CreateView):
    model = Processo
    form_class = ProcessoModelForm
    template_name = 'nonconformity/processo.html'
    success_message = 'Processo aggiunto correttamente!'
    

    def get_success_url(self):        
        
        return reverse_lazy('nonconformity:tabelle_generiche')
        
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
        }

class ProcessoUpdateView(LoginRequiredMixin, UpdateView):
    model = Processo
    form_class = ProcessoModelForm
    template_name = 'nonconformity/processo.html'
    success_message = 'Processo modificato correttamente!'
    
    
    def get_success_url(self):        
        
        return reverse_lazy('nonconformity:tabelle_generiche')
            

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        # pk_procedura = self.object.pk        
        # context['elenco_revisioni'] = RevisioneProcedura.objects.filter(fk_procedura=pk_procedura) 
        # context['elenco_moduli'] = Modulo.objects.filter(fk_procedura=pk_procedura) 

        return context



def delete_processo(request, pk): 
        deleteobject = get_object_or_404(Processo, pk = pk)                 
        deleteobject.delete()
        url_match = reverse_lazy('nonconformity:tabelle_generiche')
        return redirect(url_match)


'''Processo->Audit'''
class ProcessoAuditCreateView(LoginRequiredMixin,CreateView):
    model = ProcessoAudit
    form_class = ProcessoAuditModelForm
    template_name = 'nonconformity/processo_audit.html'
    success_message = 'Processo aggiunto correttamente!'
    

    def get_success_url(self):        
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('nonconformity:home_rapporti_audit')
        
        fk_rapportoaudit=self.object.fk_rapportoaudit.pk
        return reverse_lazy('nonconformity:modifica_rapporto_audit', kwargs={'pk':fk_rapportoaudit})
        
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_initial(self):
        created_by = self.request.user
        fk_rapportoaudit = self.kwargs['fk_rapportoaudit']
        return {
            'created_by': created_by,
            'fk_rapportoaudit': fk_rapportoaudit
        }
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        fk_rapportoaudit = self.kwargs['fk_rapportoaudit']       
        context['fk_rapportoaudit'] = RapportoAudit.objects.get(pk=fk_rapportoaudit) 
        return context
    


class ProcessoAuditUpdateView(LoginRequiredMixin, UpdateView):
    model = ProcessoAudit
    form_class = ProcessoAuditModelForm
    template_name = 'nonconformity/processo_audit.html'
    success_message = 'Processo modificato correttamente!'
    
    
    def get_success_url(self):        
        
        fk_rapportoaudit=self.object.fk_rapportoaudit.pk
        return reverse_lazy('nonconformity:modifica_rapporto_audit', kwargs={'pk':fk_rapportoaudit})
            

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        print("Tutti i kwargs:", self.kwargs)  # Stampa tutti i kwargs
        fk_rapportoaudit = self.kwargs['fk_rapportoaudit']  
        fk_processo_audit = self.kwargs['pk']
        print("Valore di fk_rapportoaudit:", fk_rapportoaudit)
        print("processi: " + str(ProcessoAudit.objects.filter(fk_rapportoaudit=fk_rapportoaudit)))

        context['fk_rapportoaudit'] = RapportoAudit.objects.get(pk=fk_rapportoaudit) 
        context['processo_audit'] = ProcessoAudit.objects.get(pk=fk_processo_audit)
        
        context['processi_audit'] = ProcessoAudit.objects.filter(fk_rapportoaudit=fk_rapportoaudit)
        # context['elenco_moduli'] = Modulo.objects.filter(fk_procedura=pk_procedura) 

        return context



def delete_processo_audit(request, pk): 
        deleteobject = get_object_or_404(ProcessoAudit, pk = pk) 
        fk_rapportoaudit = deleteobject.fk_rapportoaudit.pk                 
        deleteobject.delete()
        url_match = reverse_lazy('nonconformity:modifica_rapporto_audit', kwargs={'pk':fk_rapportoaudit})
        return redirect(url_match)