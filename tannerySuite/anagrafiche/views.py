import datetime

from articoli.models import ListinoCliente, ListinoTerzista, PrezzoListino
from django.apps import apps
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.utils import IntegrityError
from django.forms.models import modelform_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django_filters.views import FilterView
from nonconformity.models import RapportoNC

from .filters import ClienteFilter, FornitoreFilter, TransferValueFilter
from .forms import (FormCliente, FormFacility, FormFacilityContact,
                    FormFornitore, FormFornitoreLavorazioniEsterne,
                    FormFornitorePelli, FormFornitoreProdottiChimici,
                    FormFornitoreServizi, FormLwgFornitore, FormTransferValue,
                    FormXrDocumentiGestore, FormXrTransferValueLwgFornitore,
                    ListinoClienteModelForm, ListinoTerzistaModelForm,
                    PrezzoListinoModelForm)
from .models import (Cliente, Facility, FacilityContact, Fornitore,
                     FornitoreLavorazioniEsterne, FornitorePelli,
                     FornitoreProdottiChimici, FornitoreRifiuti,
                     FornitoreServizi, LwgFornitore, TransferValue,
                     XrDocumentiGestore, XrDocumentiSmaltitore,
                     XrDocumentiTrasportatore, XrTransferValueLwgFornitore)

# Create your views here.

def home_fornitori(request): 
    fornitori = Fornitore.objects.all()
    fornitori_filter = FornitoreFilter(request.GET, queryset=fornitori)
    #filterset_class = FornitoreFilter
    page = request.GET.get('page', 1)
    paginator = Paginator(fornitori_filter.qs, 50)  # Utilizza fornitori_filter.qs per la paginazione
            
    try:
        fornitori_paginator = paginator.page(page)
    except PageNotAnInteger:
        fornitori_paginator = paginator.page(1)
    except EmptyPage:
        fornitori_paginator = paginator.page(paginator.num_pages)
        
    context = {
        #'fornitori': filterset_class,
        'fornitori_paginator': fornitori_paginator,
        'filter': fornitori_filter,
        'CHOICES_CATEGORY': Fornitore.CHOICES_CATEGORY
    }
    return render(request, 'anagrafiche/home_fornitori.html', context)


class UpdateSupplier(LoginRequiredMixin, UpdateView):
    model = Fornitore
    template_name = 'anagrafiche/fornitore.html'
    form_class = FormFornitore
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()  # Utilizza il form principale per Fornitore        
        # Ottieni l'istanza di Categoria correlata al Fornitore attuale
        categoria_model_name = f'Fornitore{self.object.categoria.title().replace(" ", "")}'
        
        if categoria_model_name != 'FornitoreNessuna':
            categoria_model = apps.get_model(app_label='anagrafiche', model_name=categoria_model_name)
            
            
            if categoria_model:
                print("categoria_model:" + str(categoria_model))
                categoria_instance = categoria_model.objects.filter(fornitore_ptr=self.object).first() 
                if categoria_instance:
                    CategoriaForm = modelform_factory(categoria_model, exclude=['fornitore'])
                    nome_form_secondario = CategoriaForm.__name__            
                    context["nome_form_secondario"] = nome_form_secondario            
                    modello_form = CategoriaForm(instance=categoria_instance)            
                    context["modello_form"] = modello_form
                else:
                    context["categoria_instance_missing"] = True  # Aggiungi questa chiave al contesto
                    
        context["lwg_certs"] = LwgFornitore.objects.filter(fk_fornitore_id=self.object.pk) 
        context["nc_associate"] = RapportoNC.objects.filter(fk_fornitore=self.object.pk)
        context["listini_terzisti"] = ListinoTerzista.objects.filter(fk_fornitore=self.object.pk)
        context["gestori_rifiuti"] = XrDocumentiGestore.objects.filter(fornitore_rifiuti=self.object.pk)
        context["smaltitori_rifiuti"] = XrDocumentiSmaltitore.objects.filter(fornitore_rifiuti=self.object.pk)
        context["trasportatori_rifiuti"] = XrDocumentiTrasportatore.objects.filter(fornitore_rifiuti=self.object.pk)
        return context
    
    

    def get_success_url(self):        
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('anagrafiche:home_fornitori')
        
        pk_fornitore=self.object.pk
        return reverse_lazy('anagrafiche:vedi_fornitore', kwargs={'pk':pk_fornitore})

    
    def form_valid(self, form):        
        messages.info(self.request, 'Il fornitore è stato modificato!') # Compare sul success_url
        return super().form_valid(form)
    
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            categoria_model_name = f'Fornitore{self.object.categoria.title().replace(" ", "")}'
            if categoria_model_name != 'FornitoreNessuna':
                categoria_model = apps.get_model(app_label='anagrafiche', model_name=categoria_model_name)
                if categoria_model:
                    categoria_instance = categoria_model.objects.filter(fornitore_ptr=self.object).first()

                    if not categoria_instance:
                        categoria_instance = categoria_model.objects.create(fornitore_ptr=self.object)

                    CategoriaForm = modelform_factory(categoria_model, exclude=['fornitore'])
                    categoria_form = CategoriaForm(request.POST, instance=categoria_instance)
                    if categoria_form.is_valid():
                        categoria_form.save()

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

        
    def form_invalid(self, form):
        #messages.error(self.request, 'Errore! Il fornitore non è stato aggiunto!')
        return super().form_invalid(form)



def aggiungi_fornitore_with_category(request, category):
    context = {
        'category': category,
        'CHOICES_CATEGORY': Fornitore.CHOICES_CATEGORY,
    }
    return render(request, 'anagrafiche/aggiungi_fornitore_modal.html', context)



class CreateSupplier(LoginRequiredMixin, CreateView):
    
    model = Fornitore
    form_class = FormFornitore
    success_message = 'Fornitore aggiunto correttamente!'
    error_message = 'Error saving the Doc, check fields below.'
    template_name = "anagrafiche/fornitore.html"
    
    

    def get_initial(self):
        initial = super().get_initial()
        created_by = self.request.user
        categoria = self.request.GET.get('categoria')
        if categoria in dict(Fornitore.CHOICES_CATEGORY):
            initial['categoria'] = categoria
            print("categoria initial: " + str(categoria))
        initial['created_by']= created_by
        initial['created_at']= datetime.datetime.now()
        return initial
        
    def get_success_url(self):        
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('anagrafiche:home_fornitori')
        
        pk_fornitore=self.object.pk
        print("pk_fornitore: " + str(pk_fornitore))
        return reverse_lazy('anagrafiche:vedi_fornitore', kwargs={'pk':pk_fornitore})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['CHOICES_CATEGORY'] = Fornitore.CHOICES_CATEGORY
        return context
    
    
    def form_valid(self, form):
        forn = form.save(commit=False)
        forn.created_by = self.request.user
        forn.created_at = datetime.datetime.now()
        categoria = form.cleaned_data["categoria"]
        forn.save()

        print("categoria: " + str(categoria))

        if categoria == Fornitore.NESSUNA:  # Nessuna categoria selezionata
            forn.save()
            messages.info(self.request, 'Il fornitore è stato aggiunto!')
            self.object = forn
            return HttpResponseRedirect(self.get_success_url())

        categoria_model_name = f'Fornitore{categoria.title().replace(" ", "")}'
        print("categoria_model_name: " + str(categoria_model_name))
        categoria_model = apps.get_model(app_label='anagrafiche', model_name=categoria_model_name)

        if categoria_model:
            try:
                # Crea l'istanza del modello specifico per la categoria senza salvarla
                categoria_instance = categoria_model(fornitore_ptr=forn)

                # Aggiungi qui la mappatura tra categoria e attributo forn.fornitore_ptr_* corretto
                categoria_attr_map = {
                    'FornitorePelli': 'fornitore_ptr_pelli',
                    'FornitoreProdottiChimici': 'fornitore_ptr_prodottichimici',
                    'FornitoreManutenzioni': 'fornitore_ptr_manutenzioni',
                    'FornitoreLavorazioniEsterne': 'fornitore_ptr_lavorazioniesterne',
                    'FornitoreServizi': 'fornitore_ptr_servizi',
                    'FornitoreRifiuti': 'fornitore_ptr_rifiuti',
                    # Aggiungi altri se necessario
                }

                categoria_attr = categoria_attr_map.get(categoria_model_name)
                print("categoria_attr: " + str(categoria_attr))
                if categoria_attr:
                    setattr(forn, categoria_attr, categoria_instance)
                    categoria_instance = categoria_model.objects.create(fornitore_ptr=forn)
                    forn.save()  # Salva l'istanza del modello generico con la relazione
            except IntegrityError as e:
                forn.delete()
                messages.error(self.request, 'Errore! Il fornitore non è stato aggiunto!')
                return super().form_invalid(form)

        self.object = forn
        messages.info(self.request, 'Il fornitore è stato aggiunto!')
        return HttpResponseRedirect(self.get_success_url())


    def form_invalid(self, form):
        messages.error(self.request, 'Errore! Il fornitore non è stato aggiunto!')
        return super().form_invalid(form)


'''
class CreateSupplier(LoginRequiredMixin, CreateView):
    model = Fornitore
    form_class = FormFornitore
    success_message = 'Fornitore aggiunto correttamente!'
    error_message = 'Error saving the Doc, check fields below.'
    template_name = "anagrafiche/fornitore.html"

    def get_initial(self):
        initial = super().get_initial()
        categoria = self.request.GET.get('categoria')
        if categoria in dict(Fornitore.CHOICES_CATEGORY):
            initial['categoria'] = categoria
        initial['created_by'] = self.request.user
        initial['created_at'] = datetime.datetime.now()
        return initial

    def get_success_url(self):
        if 'salva_esci' in self.request.POST:
            return reverse_lazy('anagrafiche:home_fornitori')
        return reverse_lazy('anagrafiche:vedi_fornitore', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['CHOICES_CATEGORY'] = Fornitore.CHOICES_CATEGORY
        return context

    def form_valid(self, form):
        print("Form valido:", form.is_valid())  # Debug
        forn = form.save(commit=False)
        forn.created_by = self.request.user
        forn.created_at = datetime.datetime.now()
        categoria = form.cleaned_data["categoria"]
        
        try:
            forn.save()  # Salva l'oggetto fornitore
            print("Fornitore salvato:", forn.pk)  # Debug: conferma se il salvataggio è avvenuto
        except Exception as e:
            print(f"Errore durante il salvataggio: {e}")
            return self.form_invalid(form)

        # Assegna l'oggetto forn a self.object
        self.object = forn

        # Crea l'istanza del modello di categoria se necessario
        if categoria != Fornitore.NESSUNA:
            categoria_model_name = f'Fornitore{categoria.title().replace(" ", "")}'
            try:
                categoria_model = apps.get_model(app_label='anagrafiche', model_name=categoria_model_name)
                if categoria_model:
                    categoria_model.objects.create(fornitore_ptr=forn)
            except Exception as e:
                messages.error(self.request, 'Errore! Il fornitore non è stato aggiunto correttamente!')
                return self.form_invalid(form)

        messages.success(self.request, 'Il fornitore è stato aggiunto correttamente!')
        return HttpResponseRedirect(self.get_success_url())



    def form_invalid(self, form):
        messages.error(self.request, 'Errore! Il fornitore non è stato aggiunto!')
        return super().form_invalid(form)

'''

class AddLwgCertificate(CreateView):
    
    model = LwgFornitore
    form_class = FormLwgFornitore
    success_message = 'Certificato aggiunto correttamente!'
    error_message = 'Error saving the Doc, check fields below.'
    
    
    template_name = "anagrafiche/lwg.html"


    def get_success_url(self):          
        #fornitore=self.object.fk_fornitore.pk
            
        if 'salva_esci' in self.request.POST:
            fornitore = self.object.fk_fornitore.pk
            print("Fornitore: " + str(fornitore))
            return reverse_lazy('anagrafiche:vedi_fornitore', kwargs={'pk': fornitore})

        pk=self.object.pk        
        return reverse_lazy('anagrafiche:modifica_lwg', kwargs={'pk':pk})
    

    def get_initial(self):
        fk_fornitore = self.kwargs['fk_fornitore']
        return {
            'fk_fornitore': fk_fornitore,
            
        }
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        fk_fornitore=self.kwargs['fk_fornitore']
        print("Fornitore: " + str(fk_fornitore))
        #context['fornitore'] = Fornitore.objects.get(pk=fornitore) # FILTRARE
        context['fornitore'] = Fornitore.objects.get(pk=fk_fornitore)
        context['fk_fornitore'] = fk_fornitore
        return context

class UpdateLwgCertificate(UpdateView):
    
    model = LwgFornitore
    form_class = FormLwgFornitore
    success_message = 'Certificato modificato correttamente!'
    error_message = 'Certificato non salvato. Controlla.'    
    
    template_name = "anagrafiche/lwg.html"


    def get_success_url(self):
        if 'salva_esci' in self.request.POST:
            fornitore = self.object.fk_fornitore.pk
            print("Fornitore: " + str(fornitore))
            return reverse_lazy('anagrafiche:vedi_fornitore', kwargs={'pk': fornitore})

        pk=self.object.pk
        print(f'pk da success url: {pk}')       
        return reverse_lazy('anagrafiche:modifica_lwg', kwargs={'pk':pk})
    

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        fk_fornitore = self.object.fk_fornitore.pk
        context['transfer_values'] = XrTransferValueLwgFornitore.objects.filter(fk_lwgcertificato=self.object.id) 
        context['fk_fornitore'] = fk_fornitore
        context['fornitore'] = Fornitore.objects.get(pk=fk_fornitore)        
        
        return context



def delete_certificato(request, pk): 
        deleteobject = get_object_or_404(LwgFornitore, pk = pk)
        fornitore=deleteobject.fk_fornitore.pk   
        #dettaglio=deleteobject.iddettordine           
        #linea = deleteobject.id_linea  
        #tempomaster=deleteobject.idtempomaster      
        deleteobject.delete()
        url_match= reverse_lazy('anagrafiche:vedi_fornitore', kwargs={'pk': fornitore})
        return redirect(url_match)



class XrTransferValueCreateView(CreateView):
    model = XrTransferValueLwgFornitore
    form_class = FormXrTransferValueLwgFornitore
    success_message = 'Transfer Value modificata correttamente!'
    # success_url = reverse_lazy('anagrafiche:modifica_lwg')
    template_name = "anagrafiche/lwg_transfer_values.html"

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        fk_certificato = self.kwargs['fk_certificato']
        print(f'fk_certificato: {fk_certificato}')
        certificato=LwgFornitore.objects.get(pk=fk_certificato)
        fornitore=Fornitore.objects.get(pk=certificato.fk_fornitore.pk)
        context['fornitore'] = fornitore
        context['certificato'] = certificato
        
        return context

    def get_initial(self):        
        fk_certificato = self.kwargs['fk_certificato']
        certificato=LwgFornitore.objects.get(pk=fk_certificato)        
        created_by = self.request.user
        return {
            'fk_lwgcertificato': certificato.pk,
            'created_by': created_by            
        }
    
    def get_success_url(self):
        fk_certificato=self.object.fk_lwgcertificato.pk              
        return reverse_lazy('anagrafiche:modifica_lwg', kwargs={'pk':fk_certificato})
    
    
class XrTransferValueUpdateView(LoginRequiredMixin,UpdateView):
    model = XrTransferValueLwgFornitore
    form_class = FormXrTransferValueLwgFornitore
    template_name = 'anagrafiche/lwg_transfer_values.html'
    success_message = 'Transfer Value modificata correttamente!'
    success_url = reverse_lazy('anagrafiche:modifica_lwg')

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)        
        xrtv = XrTransferValueLwgFornitore.objects.get(pk=self.kwargs['pk'])
        fk_certificato=xrtv.fk_lwgcertificato.pk
        certificato=LwgFornitore.objects.get(pk=fk_certificato)
        fornitore=Fornitore.objects.get(pk=certificato.fk_fornitore.pk)
        context['fornitore'] = fornitore
        context['certificato'] = certificato
        return context

    def get_success_url(self):        
        lwgcertificate=self.object.fk_lwgcertificato.pk
        return reverse_lazy('anagrafiche:modifica_lwg', kwargs={'pk': lwgcertificate})
    
    
def delete_xrtransfervalue(request, pk): 
        deleteobject = get_object_or_404(XrTransferValueLwgFornitore, pk = pk)         
        fk_certificato=deleteobject.fk_lwgcertificato.pk       
        deleteobject.delete()
        url_match= reverse_lazy('anagrafiche:modifica_lwg', kwargs={'pk': fk_certificato})
        return redirect(url_match)    


class ListaFornitoriView(FilterView):

        model = Fornitore
        context_object_name = 'initial_fornitori'
        template_name = "anagrafiche/home_fornitori.html"
        filterset_class = FornitoreFilter
        paginate_by = 30
        # ordering = ['-iddettordine']
        
def aggiungi_facility_details(request, pk):
    facility = get_object_or_404(Facility, pk=pk)
    if request.method == "POST":
        form = FormFacility(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.facility = facility
        else:
            form = FormFacility()
        context = {'facility': facility, 'form': form}
        
        return render(request, "anagrafiche/facility.html", context)
    
    
class FacilityCreateView(CreateView):
    template_name = 'anagrafiche/facility.html'
    form_class = FormFacility
    
class FacilityUpdateView(UpdateView):
    model = Facility
    template_name = 'anagrafiche/facility.html'
    form_class = FormFacility
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)        
        context['facility_contacts'] = FacilityContact.objects.filter(fk_facility=self.object.pk)        
        return context

    

def add_facility_contact(request, pk):
    facility = get_object_or_404(Facility, pk=pk)
    
    if request.method == "POST":
        form = FormFacilityContact(request.POST)
        fk_facility = facility
        nome_cognome = request.POST.get("name")
        contact_type = request.POST.get("contact_type")
        position = request.POST.get("position")
        facility_contact = FacilityContact.objects.create(name=nome_cognome, 
                                                            contact_type=contact_type,
                                                            position=position,
                                                            fk_facility=fk_facility
                                                            )
        messages.info(request, 'Il contatto è stato aggiunto!')
        return redirect('anagrafiche:edit_facility_details', pk=pk)
    else:
        form = FormFacilityContact()

    return render(request, 'anagrafiche/facility_contacts.html', {'facility': facility, 'form': form})
    
    
class FacilityContactUpdateView(LoginRequiredMixin, UpdateView):
    model = FacilityContact
    form_class = FormFacilityContact
    template_name = 'anagrafiche/facility_contacts.html'
    success_message = 'Contatto modificato correttamente!'
    #success_url = reverse_lazy('human_resources:tabelle_generiche_formazione')
    
    def get_success_url(self):                
        fk_facility=self.object.fk_facility.pk        
        return reverse_lazy('anagrafiche:edit_facility_details', kwargs={'pk':fk_facility})

def delete_facility_contact(request, pk): 
        deleteobject = get_object_or_404(FacilityContact, pk = pk)         
        fk_facility=deleteobject.fk_facility.pk       
        deleteobject.delete()
        messages.warning(request, 'Voce eliminata correttamente!')
        url_match= reverse_lazy('anagrafiche:edit_facility_details', kwargs={'pk':fk_facility})
        return redirect(url_match)    

# Creazione, Vista e Update Clienti
class ClienteCreateView(LoginRequiredMixin,CreateView):
    model = Cliente
    form_class = FormCliente
    template_name = 'anagrafiche/cliente.html'
    success_message = 'Cliente aggiunto correttamente!'
    success_url = reverse_lazy('anagrafiche:home_clienti')
    
    def get_initial(self):
        created_by = self.request.user
        return {
            'created_by': created_by,
            'created_at': datetime.datetime.now() 
        }
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    

class ClienteUpdateView(LoginRequiredMixin,UpdateView):
    model = Cliente
    form_class = FormCliente
    template_name = 'anagrafiche/cliente.html'
    success_message = 'Cliente modificato correttamente!'
    success_url = reverse_lazy('anagrafiche:home_clienti')

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        fk_cliente=self.kwargs['pk']
        listini=ListinoCliente.objects.filter(fk_cliente=fk_cliente)        
        context['listini'] = listini
        return context
    
    
class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'anagrafiche/home_clienti.html'
    paginate_by = 10


class ListaClienteView(FilterView):

        model = Cliente
        context_object_name = 'initial_clienti'
        template_name = "anagrafiche/home_clienti.html"
        filterset_class = ClienteFilter
        paginate_by = 30





'''SEZIONE TABELLE GENERICHE'''


def tabelle_generiche(request):
    transfervalues = TransferValue.objects.all()
    tot_transfervalues = TransferValue.objects.count()
    
    transfervalues_filter = TransferValueFilter(request.GET, queryset=transfervalues)
    filtered_transfervalues = transfervalues_filter.qs  # Ottieni i record filtrati
    transfervalues_filter_count = filtered_transfervalues.count()  # Conta i record filtrati
    

    '''sostanze_filter = SostanzaFilter(request.GET, queryset=sostanze)
    filtered_sostanze = sostanze_filter.qs  # Ottieni i record filtrati
    sostanze_filter_count = filtered_sostanze.count()  # Conta i record filtrati'''


    # Paginazione Sostanze
    page_transfervalues = request.GET.get('page', 1)
    paginator_transfervalues = Paginator(filtered_transfervalues, 50)
    
    try:
        transfervalues_paginator = paginator_transfervalues.page(page_transfervalues)
    except PageNotAnInteger:
        transfervalues_paginator = paginator_transfervalues.page(1)
    except EmptyPage:
        transfervalues_paginator = paginator_transfervalues.page(paginator_transfervalues.num_pages)

   


    context = {
        # Transfer Values
        'transfervalues': transfervalues,
        'transfervalues_paginator': transfervalues_paginator,
        'tot_transfervalues': tot_transfervalues,
        'filter_transfervalues': transfervalues_filter,
        'transfervalues_filter_count': transfervalues_filter_count,
    }
    
    return render(request, 'anagrafiche/generiche/tabelle_generiche.html', context)

# Creazione, Vista e Update Transfer Values
class TransferValueCreateView(LoginRequiredMixin,CreateView):
    model = TransferValue
    form_class = FormTransferValue
    template_name = 'anagrafiche/transfer_value.html'
    success_message = 'Transfer Value aggiunta correttamente!'
    success_url = reverse_lazy('anagrafiche:tabelle_generiche')

    

class TransferValueUpdateView(LoginRequiredMixin,UpdateView):
    model = TransferValue
    form_class = FormTransferValue
    template_name = 'anagrafiche/transfer_value.html'
    success_message = 'Transfer Value modificata correttamente!'
    success_url = reverse_lazy('anagrafiche:tabelle_generiche')

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)


def delete_transfer_value(request, pk): 
        deleteobject = get_object_or_404(TransferValue, pk = pk)         
        deleteobject.delete()
        messages.warning(request, 'Voce eliminata correttamente!')
        url_match= reverse_lazy('anagrafiche:tabelle_generiche') 
        return redirect(url_match)    

'''FINE SEZIONE TABELLE GENERICHE'''
    


'''SEZIONE AUTORIZZAZIONI'''
'''


def home_autorizzazioni(request, fk_facility):
    autorizzazioni = FacilityAuthorization.objects.filter(fk_facility=fk_facility)
    autorizzazioni_filter = FacilityAuthorizationFilter(request.GET, queryset=autorizzazioni)
    fk_facility = fk_facility
    facility = Facility.objects.get(pk=fk_facility)
    
    page = request.GET.get('page', 1)
    paginator = Paginator(autorizzazioni_filter.qs, 50)  # Utilizza fornitori_filter.qs per la paginazione

    try:
        autorizzazioni_paginator = paginator.page(page)
    except PageNotAnInteger:
        autorizzazioni_paginator = paginator.page(1)
    except EmptyPage:
        autorizzazioni_paginator = paginator.page(paginator.num_pages)

    context = {
        
        'autorizzazioni_paginator': autorizzazioni_paginator,
        'filter': autorizzazioni_filter,
        'fk_facility': fk_facility,
        'facility': facility
        
    }
    return render(request, 'anagrafiche/home_autorizzazioni.html', context)

class FacilityAuthorizationCreateView(LoginRequiredMixin,CreateView):
    model = FacilityAuthorization
    form_class = FacilityAuthorizationModelForm
    template_name = 'anagrafiche/autorizzazione.html'
    success_message = 'Autorizzazione aggiunta correttamente!'
    

    def get_success_url(self):                
        fk_facility=self.object.fk_facility.pk       
        if 'salva_esci' in self.request.POST:                        
                return reverse_lazy('anagrafiche:edit_facility_details', kwargs={'pk':fk_facility})
        
        pk_autorizzazione=self.object.pk        
        return reverse_lazy('anagrafiche:modifica_facility_authorization', kwargs={'fk_facility':fk_facility, 'id':pk_autorizzazione})
    
    
    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        facility = Facility.objects.get(pk=self.kwargs['fk_facility'])
        
        
        context['facility'] = facility
        
        
        return context

    

    def get_initial(self):
        created_by = self.request.user
        #fk_facility = self.kwargs['fk_facility'] 
        facility = Facility.objects.get(pk=self.kwargs['fk_facility'])
        print(f'fk_facility: {facility.pk}')
        #facility = Facility.objects.get(pk=fk_facility)
        return {
            'created_by': created_by,
            'fk_facility': facility.pk,
            'facility': facility            
        }

class FacilityAuthorizationUpdateView(LoginRequiredMixin, UpdateView):
    model = FacilityAuthorization
    form_class = FacilityAuthorizationModelForm
    template_name = 'anagrafiche/autorizzazione.html'
    success_message = 'Autorizzazione modificata correttamente!'
    
    
    def get_success_url(self):    
        fk_facility=self.object.fk_facility.pk       
        if 'salva_esci' in self.request.POST:                        
                return reverse_lazy('anagrafiche:edit_facility_details', kwargs={'pk':fk_facility})
        
        pk_autorizzazione=self.object.pk        
        return reverse_lazy('anagrafiche:modifica_facility_authorization', kwargs={'fk_facility':fk_facility, 'id':pk_autorizzazione})
    

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        pk_facility = self.object.pk

        context['elenco_revisioni'] = DetailFacilityAuthorization.objects.filter(fk_facility_authorization=pk_facility) 
        context['facility']=Facility.objects.get(pk=pk_facility)

        # context['elenco_moduli'] = Modulo.objects.filter(fk_procedura=pk_procedura) 

        return context


def delete_facility_authorization(request, pk): 
        deleteobject = get_object_or_404(FacilityAuthorization, pk = pk)                 
        deleteobject.delete()
        url_match = reverse_lazy('anagrafiche:edit_facility_details')
        return redirect(url_match)
    '''
'''FINE SEZIONE AUTORIZZAZIONI'''



class ListinoTerzistaCreateView(CreateView):
    
    model = ListinoTerzista
    form_class = ListinoTerzistaModelForm
    success_message = 'Voce listino aggiunta correttamente!'
    error_message = 'Error saving the Doc, check fields below.'
    
    
    template_name = "anagrafiche/voce_listino.html"


    def get_success_url(self):          
        #fornitore=self.object.fk_fornitore.pk
            
        if 'salva_esci' in self.request.POST:
            pk_fornitore = self.object.fk_fornitore.pk
            
            
            return reverse_lazy('anagrafiche:vedi_fornitore', kwargs={'pk': pk_fornitore})

        pk=self.object.pk        
        return reverse_lazy('anagrafiche:modifica_voce_listino', kwargs={'pk':pk})
    

    def get_initial(self):
        initial = super().get_initial() 
        fk_fornitore = self.kwargs['fk_fornitore']
        created_by = self.request.user
        
        initial['created_by'] = created_by
        initial['fk_fornitore'] = fk_fornitore
        return initial
        
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        print("kwargs:", kwargs)
        fk_fornitore=self.kwargs['fk_fornitore']
        print("Fornitore: " + str(fk_fornitore))        
        context['fk_fornitore'] = fk_fornitore
        return context

class ListinoTerzistaUpdateView(UpdateView):
    
    model = ListinoTerzista
    form_class = ListinoTerzistaModelForm
    success_message = 'Voce listino modificata correttamente!'
    error_message = 'Certificato non salvato. Controlla.'    
    
    template_name = "anagrafiche/voce_listino.html"


    def get_success_url(self):
        if 'salva_esci' in self.request.POST:
            fornitore = self.object.fk_fornitore.pk
            print("Fornitore: " + str(fornitore))
            return reverse_lazy('anagrafiche:vedi_fornitore', kwargs={'pk': fornitore})

        pk=self.object.pk
        print(f'pk da success url: {pk}')       
        return reverse_lazy('anagrafiche:modifica_voce_listino', kwargs={'pk':pk})
    

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        fk_fornitore = self.object.fk_fornitore.pk
        #context['transfer_values'] = XrTransferValueLwgFornitore.objects.filter(fk_lwgcertificato=self.object.id) 
        context['fk_fornitore'] = fk_fornitore
        context['listino']=self.kwargs['pk']
        context['fornitore'] = Fornitore.objects.get(pk=fk_fornitore)  
        context['prezzi']=PrezzoListino.objects.filter(fk_listino_terzista=self.object.pk)      
        
        return context



def delete_voce_listino(request, pk): 
        deleteobject = get_object_or_404(ListinoTerzista, pk = pk)
        fornitore=deleteobject.fk_fornitore.pk   
        #dettaglio=deleteobject.iddettordine           
        #linea = deleteobject.id_linea  
        #tempomaster=deleteobject.idtempomaster      
        deleteobject.delete()
        messages.warning(request, 'Voce eliminata correttamente!')
        url_match= reverse_lazy('anagrafiche:vedi_fornitore', kwargs={'pk': fornitore})
        return redirect(url_match)


# Prezzo Listino
class PrezzoListinoCreateView(CreateView):
    
    model = PrezzoListino
    form_class = PrezzoListinoModelForm
    success_message = 'Prezzo aggiunto correttamente!'
    error_message = 'Error saving the Doc, check fields below.'
    
    
    template_name = "anagrafiche/prezzo_listino.html"

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    
    def get_success_url(self):
        fk_listino_terzista = self.object.fk_listino_terzista.pk  
        print(f"fk_listino_terzista_success: {fk_listino_terzista}")      
        return reverse_lazy('anagrafiche:modifica_voce_listino', kwargs={'pk': fk_listino_terzista})


    def get_initial(self):
        initial = super().get_initial() 
        created_by = self.request.user
        fk_listino_terzista = self.kwargs['fk_listino_terzista']        
        initial['fk_listino_terzista'] = fk_listino_terzista
        initial['created_by'] = created_by
        return initial
        
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        print("kwargs:", kwargs)
        
        fk_listino_terzista=self.kwargs['fk_listino_terzista']
        print(f'fk_listino_terzista: {fk_listino_terzista}')
        listino_terzista = ListinoTerzista.objects.get(pk=fk_listino_terzista)
        fk_fornitore = listino_terzista.fk_fornitore.pk
        print(f"fk_fornitore: {fk_fornitore}")
        print("fk_listino_terzista: " + str(fk_listino_terzista))
        context['fk_fornitore']=fk_fornitore
        context['fk_listino_terzista'] = fk_listino_terzista
        return context

class PrezzoListinoUpdateView(UpdateView):
    
    model = PrezzoListino
    form_class = PrezzoListinoModelForm
    success_message = 'Prezzo modificato correttamente!'
    error_message = 'Prezzo non salvato. Controlla.'    
    
    template_name = "anagrafiche/prezzo_listino.html"


    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)
    
    def get_success_url(self):    
        fk_listino_terzista = self.object.fk_listino_terzista.pk        
        return reverse_lazy('anagrafiche:modifica_voce_listino', kwargs={'pk': fk_listino_terzista})

    

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        fk_listino_terzista = self.object.fk_listino_terzista        
        context['fk_listino_terzista'] = fk_listino_terzista
        context['listino'] = ListinoTerzista.objects.get(pk=fk_listino_terzista)        
        
        return context



def delete_prezzo_listino(request, pk): 
        deleteobject = get_object_or_404(PrezzoListino, pk = pk)
        fk_listino_terzista=deleteobject.fk_listino_terzista_id               
        deleteobject.delete()
        messages.warning(request, 'Voce eliminata correttamente!')
        url_match= reverse_lazy('anagrafiche:modifica_voce_listino', kwargs={'pk': fk_listino_terzista})
        return redirect(url_match)



# XR DocumentiGestori rifiuti

class XrDocumentiGestoreCreateView(CreateView):
    
    model = XrDocumentiGestore
    form_class = FormXrDocumentiGestore
    success_message = 'Documento Gestore aggiunto correttamente!'
    error_message = 'Error saving the Doc, check fields below.'
    
    
    template_name = "anagrafiche/gestori_rifiuti.html"


    def get_success_url(self):          
       # fornitore=self.object.fk_fornitore.pk
        pk=self.object.pk        
        return reverse_lazy('anagrafiche:vedi_fornitore', kwargs={'pk':pk})
    

    def get_initial(self):
        initial = super().get_initial()
        print(f'Iniziale: {initial}')
        created_by = self.request.user
        print(f'kwargs: {self.kwargs}')
        # Aggiungi l'ID del fornitore_rifiuti passato dall'URL
        # fornitore_rifiuti = get_object_or_404(FornitoreRifiuti, fornitore_ptr=self.kwargs['fk_fornitore'])
        fornitore_rifiuti = get_object_or_404(FornitoreRifiuti, fornitore_ptr_id=self.kwargs['fk_fornitore'])
        provafornitorerifiuti=FornitoreRifiuti.objects.filter(fornitore_ptr_id=211)
        for rifiuti in provafornitorerifiuti:
            print(f'ID: {rifiuti.id}') 
        print(f'Fornitore rifiuti in get_initial: {fornitore_rifiuti}')
        print(f'Fornitore rifiuti pk in get_initial: {fornitore_rifiuti.pk}')
        initial['fornitore_rifiuti'] = fornitore_rifiuti.pk  # Passa solo la PK
        initial['created_by'] = created_by
        print(f'Initial: {initial}')
        return initial

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        print(f'Contesto: {context}')
        fk_fornitore=self.kwargs['fk_fornitore']
        print("Fornitore: " + str(fk_fornitore))
        fornitore = get_object_or_404(FornitoreRifiuti, fornitore_ptr_id=self.kwargs['fk_fornitore'])
        fornitore_rifiuti=get_object_or_404(FornitoreRifiuti, id=fornitore.pk)
        print(f'Fornitore pk dal contesto: {fornitore_rifiuti.pk}')
        #context['fornitore'] = Fornitore.objects.get(pk=fk_fornitore)
        #context['fornitore_rifiuti'] = self.kwargs['fk_fornitore']
        #context['fk_fornitore'] = fk_fornitore
        context['fornitore'] = fornitore_rifiuti
        context['fornitore_rifiuti'] = fornitore_rifiuti.pk
        context['fk_fornitore'] = fk_fornitore
        print(f'Contesto alla fine: {context}')
        return context
    
    def form_valid(self, form):
        # Imposta fornitore_rifiuti prima di salvare
        print(f'fornitore_rifiuti: {form.cleaned_data["fornitore_rifiuti"]}') 
        form.instance.fornitore_rifiuti = get_object_or_404(FornitoreRifiuti, fornitore_ptr=self.kwargs['fk_fornitore'])
        return super().form_valid(form)

class XrDocumentiGestoreUpdateView(UpdateView):
    
    model = XrDocumentiGestore
    form_class = FormXrDocumentiGestore
    success_message = 'Documento Gestore modificato correttamente!'
    error_message = 'Documento Gestore non salvato. Controlla.'    
    
    template_name = "anagrafiche/gestori_rifiuti.html"


    def get_success_url(self):
        if 'salva_esci' in self.request.POST:
            fornitore = self.object.fk_fornitore.pk
            print("Fornitore: " + str(fornitore))
            return reverse_lazy('anagrafiche:vedi_fornitore', kwargs={'pk': fornitore})

        pk=self.object.pk
        print(f'pk da success url: {pk}')       
        return reverse_lazy('anagrafiche:modifica_gestore_rifiuti', kwargs={'pk':pk})
    

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        fk_fornitore = self.object.fk_fornitore.pk        
        context['fk_fornitore'] = fk_fornitore
        context['fornitore'] = Fornitore.objects.get(pk=fk_fornitore)        
        
        return context



def delete_gestore_rifiuti(request, pk): 
        deleteobject = get_object_or_404(XrDocumentiGestore, pk = pk)
        fornitore=deleteobject.fk_fornitore.pk   
        #dettaglio=deleteobject.iddettordine           
        #linea = deleteobject.id_linea  
        #tempomaster=deleteobject.idtempomaster      
        deleteobject.delete()
        url_match= reverse_lazy('anagrafiche:delete_gestore_rifiuti', kwargs={'pk': fornitore})
        return redirect(url_match)




# Listino Cliente

class ListinoClienteCreateView(CreateView):
    
    model = ListinoCliente
    form_class = ListinoClienteModelForm
    success_message = 'Voce listino aggiunta correttamente!'
    
    template_name = "anagrafiche/voce_listino_cliente.html"

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_success_url(self):          
        #fornitore=self.object.fk_fornitore.pk
            
        if 'salva_esci' in self.request.POST:
            pk_cliente = self.object.fk_cliente.pk
            
            
            return reverse_lazy('anagrafiche:modifica_cliente', kwargs={'pk': pk_cliente})

        pk=self.object.pk        
        return reverse_lazy('anagrafiche:modifica_voce_listino_cliente', kwargs={'pk':pk})
    

    def get_initial(self):
        initial = super().get_initial() 
        fk_cliente = self.kwargs['fk_cliente']
        created_by = self.request.user
        
        initial['created_by'] = created_by
        initial['fk_cliente'] = fk_cliente
        return initial
        
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)        
        fk_cliente=self.kwargs['fk_cliente']                
        context['fk_cliente'] = fk_cliente
        return context

class ListinoClienteUpdateView(UpdateView):
    
    model = ListinoCliente
    form_class = ListinoClienteModelForm
    success_message = 'Voce listino modificata correttamente!'
    
    
    template_name = "anagrafiche/voce_listino_cliente.html"

    def form_valid(self, form):        
        messages.info(self.request, self.success_message) # Compare sul success_url
        return super().form_valid(form)

    def get_success_url(self):
        if 'salva_esci' in self.request.POST:
            pk_cliente = self.object.fk_cliente.pk            
            return reverse_lazy('anagrafiche:modifica_cliente', kwargs={'pk': pk_cliente})

        pk=self.object.pk            
        return reverse_lazy('anagrafiche:modifica_voce_listino_cliente', kwargs={'pk':pk})
    

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        fk_cliente = self.object.fk_cliente.pk
        context['fk_cliente'] = fk_cliente        
        context['cliente'] = Cliente.objects.get(pk=fk_cliente)  
        return context



def delete_voce_listino_cliente(request, pk): 
        deleteobject = get_object_or_404(ListinoCliente, pk = pk)
        pk_cliente=deleteobject.fk_cliente.pk   
        deleteobject.delete()
        messages.warning(request, 'Voce eliminata correttamente!')
        url_match= reverse_lazy('anagrafiche:modifica_cliente', kwargs={'pk': pk_cliente})
        return redirect(url_match)