from articoli.models import (Articolo, Lavorazione, ListinoCliente,
                             ListinoTerzista, PrezzoListino)
from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from .models import (Cliente, Facility, FacilityContact, Fornitore,
                    FornitoreLavorazioniEsterne, FornitoreManutenzioni,
                    FornitorePelli, FornitoreProdottiChimici,
                    FornitoreRifiuti, FornitoreServizi, LwgFornitore, Macello,
                    TransferValue, XrDocumentiGestore, XrDocumentiSmaltitore,
                    XrDocumentiTrasportatore, XrTransferValueLwgFornitore,
                    DestinazioneDiversaFornitore,
                    )


class FormFornitore(forms.ModelForm):
    categoria = forms.ChoiceField(choices=Fornitore.CHOICES_CATEGORY, widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Fornitore
        #exclude=()
        fields='__all__'
        ragionesociale = forms.CharField(max_length=100, label="Facility Name")
        indirizzo = forms.CharField()
        cap = forms.CharField()
        city = forms.CharField()
        provincia = forms.CharField()
        country = CountryField().formfield()
        # categoria = forms.ChoiceField(choices=Fornitore.CHOICES_CATEGORY, widget=forms.Select)        
        
        sito_web = forms.CharField()
        e_mail = forms.EmailField()
        created_at=forms.DateInput()
        
        widgets = {'country': CountrySelectWidget(),
                    'created_by': forms.HiddenInput(),
                    #'created_at': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
                    #'created_at': forms.HiddenInput(),
                    #'categoria': forms.TextInput(attrs={'readonly': 'readonly'})
                }
        labels = {
            'ragionesociale': 'Ragione Sociale',
            'country': 'Paese',
            'city': 'Città',    
            'e_mail': 'E-Mail',        
            'sito_web': 'Sito Web'
            
        }
        
class DestinazioneDiversaFornitoreModelForm(forms.ModelForm):
    

    class Meta:
        model = DestinazioneDiversaFornitore
        #exclude=()
        fields='__all__'
        
        
        
        widgets = {
                    'fk_fornitore': forms.HiddenInput(),
                    'ragionesociale': forms.TextInput(),
                    'indirizzo': forms.TextInput(),
                    'cap': forms.TextInput(),
                    'city': forms.TextInput(),
                    'provincia': forms.TextInput(),
                    'country': CountrySelectWidget(),                    
                    'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
                    'created_by': forms.HiddenInput(),
                    'created_at': forms.HiddenInput()
                    
                    
                }
        labels = {
            'ragionesociale': 'Ragione Sociale',
            'indirizzo': 'Indirizzo',
            'cap': 'CAP',
            'city': 'Città',    
            'provincia': 'Provincia',    
            'country': 'Paese',
            'note': 'Annotazioni'
            
            
        }
        
        
class FormXrDocumentiGestore(forms.ModelForm):
    class Meta:
        model = XrDocumentiGestore
        fields= '__all__'

        widgets = {
            'numero': forms.TextInput(attrs={'placeholder': 'Inserisci il numero dell\'autorizzazione...'}),
            'data_documento': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}), 
            'data_scadenza': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}), 
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput(),
            #'fornitore_rifiuti': forms.HiddenInput(),
        }
        labels = {
            'numero': 'Numero Autorizzazione',
            'data_documento': 'Data Autorizzazione', 
            'data_scadenza': 'Scadenza',
            'note': 'Note'
        }


class FormLwgFornitore(forms.ModelForm):
    class Meta:
        model = LwgFornitore
        fields= '__all__'
        
        widgets = {
            'lwg_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
            'lwg_expiry': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
            'fk_fornitore': forms.HiddenInput()
        }
        labels = {
            'lwg_urn': 'URN',
            'lwg_score': 'Punteggio',
            'lwg_range': 'Fase',
            'lwg_date': 'Data Certificato',
            'lwg_expiry': 'Scadenza Certificato',
            'documento': 'Associa Certificato'

        }
        
'''FORMS PER LA GESTIONE DEI MODELLI ASSOCIATI ALLE CATEGORIE'''
class FormFornitorePelli(forms.ModelForm):
    is_lwg = forms.BooleanField(widget=forms.CheckboxInput(), label='LWG')
    
    urn = forms.CharField(label='URN')
    tipo_fornitore = forms.CharField(label='Tipo Fornitore')
    latitude = forms.FloatField(label='Latitudine')
    longitude = forms.FloatField(label='Longitudine')

    class Meta:
        model = FornitorePelli
        fields = '__all__'

class FormFornitoreLavorazioniEsterne(forms.ModelForm):
    class Meta:
        model = FornitoreLavorazioniEsterne
        fields = '__all__'

class FormFornitoreProdottiChimici(forms.ModelForm):
    class Meta:
        model = FornitoreProdottiChimici
        fields = '__all__'

class FormFornitoreServizi(forms.ModelForm):
    class Meta:
        model = FornitoreServizi
        fields = '__all__'
        
class FormFornitoreRifiuti(forms.ModelForm):
    class Meta:
        model = FornitoreRifiuti
        fields = '__all__'

class FormFornitoreManutenzioni(forms.ModelForm):
    class Meta:
        model = FornitoreManutenzioni
        fields = '__all__'



class FormMacello(forms.ModelForm):
    

    class Meta:
        model = Macello
        #exclude=()
        fields='__all__'
        ragionesociale = forms.CharField(max_length=100, label="Facility Name")
        indirizzo = forms.CharField()
        cap = forms.CharField()
        city = forms.CharField()
        provincia = forms.CharField()
        country = CountryField().formfield()
        # categoria = forms.ChoiceField(choices=Fornitore.CHOICES_CATEGORY, widget=forms.Select)        
        
        sito_web = forms.CharField()
        e_mail = forms.EmailField()
        created_at=forms.DateInput()
        
        widgets = {'country': CountrySelectWidget(),
                    'created_by': forms.HiddenInput(),                    
                    #'created_at': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
                    #'created_at': forms.HiddenInput(),
                    #'categoria': forms.TextInput(attrs={'readonly': 'readonly'})
                }
        labels = {
            'ragionesociale': 'Ragione Sociale',
            'country': 'Paese',
            'city': 'Città',    
            'e_mail': 'E-Mail',        
            'sito_web': 'Sito Web',
            'is_group': 'Raccoglitore'
            
        }



'''FINE FORMS PER LA GESTIONE DEI MODELLI DELLE CATEGORIE ASSOCIATE'''

class FormXrTransferValueLwgFornitore(forms.ModelForm):
    class Meta:
        model = XrTransferValueLwgFornitore
        fields = '__all__'
        widgets = {'fk_lwgcertificato': forms.HiddenInput(),
                    'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
                    'created_by': forms.HiddenInput(),
                   } 
        
        labels = {
            'fk_transfervalue': 'Descrizione',
            'quantity': 'Quantità',
            'note': 'Annotazioni'
        }

class FormTransferValue(forms.ModelForm):
    class Meta:
        model = TransferValue
        fields = '__all__'



class FormFacility(forms.ModelForm):
    class Meta:
        model = Facility
        exclude=()
        #fields='__all__'
        nome_sito = forms.CharField(max_length=100, label="Facility Name")
        urn = forms.CharField(max_length=50, label="URN Number")
        piva = forms.CharField(max_length=11)
        indirizzo = forms.CharField(max_length=100)
        cap = forms.CharField(max_length=5)
        city = forms.CharField(max_length=100)
        provincia = forms.CharField(max_length=2)
        country = CountryField().formfield()
        phone = forms.CharField(max_length=50)
        primary_cat = forms.CharField(label="Categoria primaria")
        secondary_cat = forms.CharField(label="Categoria secondaria")
        tertiary_cat = forms.CharField(label="Categoria terziaria")
        latitude = forms.FloatField()
        longitude = forms.FloatField()
        site_area = forms.FloatField()
        facility_description= forms.Textarea()
        created_at = forms.DateTimeField()
        widgets = {'country': CountrySelectWidget(),
                   'created_at': forms.HiddenInput(),
                   'nome_sito': forms.TextInput(attrs={'placeholder': 'Inserisci nome azienda'}),
                   'urn': forms.TextInput(attrs={'placeholder': 'Inserisci URN'}),
                   'facility_description': forms.Textarea(attrs={'placeholder': 'Inserisci una descrizione per l\'azienda'}),
                   }
        labels = {
            'nome_sito': 'Facility Name',
            'country': 'Paese',
            'primary_cat': 'Categoria Primaria',
            'secondary_cat': 'Categoria Secondaria',
            'tertiary_cat': 'Categoria Terziaria',
            'site_area': 'Superficie del Sito',
            'latitude': 'Latitudine',
            'longitude': 'Longitudine',
            'facility_description': 'Descrizione Azienda'
        }
        
class FormFacilityContact(forms.ModelForm):
    class Meta:
        model = FacilityContact
        exclude=()
        fk_facility = forms.IntegerField()
        contact_type = forms.CharField(max_length=100)
        name = forms.CharField(max_length=100)
        position = forms.CharField(max_length=100)
        email = forms.EmailField()
        widgets = {'fk_facility': forms.HiddenInput(),
                   'name': forms.TextInput(attrs={'placeholder': 'Nome e cognome'}),
                   'position': forms.TextInput(attrs={'placeholder': 'posizione'}),
                   
                   }

class FormCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        exclude=()
        #fields='__all__'
        ragionesociale = forms.CharField(max_length=100, label="Facility Name")
        indirizzo = forms.CharField()
        cap = forms.CharField()
        city = forms.CharField()
        provincia = forms.CharField()
        country = CountryField().formfield()
        
        created_by = forms.CharField()
        created_at = forms.DateTimeField()
        widgets = {'country': CountrySelectWidget(),
                'created_at': forms.HiddenInput(),
                'created_by': forms.HiddenInput()
                }
        labels = {
            'ragionesociale': 'Ragione Sociale',
            'country': 'Paese',
            'city': 'Città',
            
            
        }
        
        
class FormMacello(forms.ModelForm):
    
    class Meta:
        model = Macello
        #exclude=()
        fields='__all__'
        ragionesociale = forms.CharField(max_length=100, label="Facility Name")
        indirizzo = forms.CharField()
        cap = forms.CharField()
        city = forms.CharField()
        provincia = forms.CharField()
        country = CountryField().formfield()
        # categoria = forms.ChoiceField(choices=Fornitore.CHOICES_CATEGORY, widget=forms.Select)        
        
        sito_web = forms.CharField()
        e_mail = forms.EmailField()
        created_at=forms.DateInput()
        is_group = forms.BooleanField()
        
        widgets = {'country': CountrySelectWidget(),
                    'created_by': forms.HiddenInput(),                   
                }
        labels = {
            'ragionesociale': 'Ragione Sociale',
            'country': 'Paese',
            'city': 'Città',    
            'e_mail': 'E-Mail',        
            'sito_web': 'Sito Web',
            'is_group': 'Raccoglitore'
            
        }

     
class ListinoTerzistaModelForm(forms.ModelForm):
    
    class Meta:
        model = ListinoTerzista
        #exclude=()
        fields='__all__'
        
        '''
        fk_lavorazione_esterna = forms.ModelChoiceField(
            queryset=LavorazioneEsterna.objects.all(),
            label='Lavorazione'),

        fk_fornitore_lavorazione_esterna = forms.ModelChoiceField(
            queryset=FornitoreLavorazioniEsterne.objects.all(),
            label='Fornitore')
        '''
        fields = ['fk_lavorazione', 'fk_fornitore', 'note', 'created_by']
        widgets = {'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
                    'created_by': forms.HiddenInput(),
                    'fk_fornitore': forms.HiddenInput()
                }
        labels = {
            'note': 'Note',
            'fk_lavorazione': 'Codice Lavorazione'
            
        }


class PrezzoListinoModelForm(forms.ModelForm):
    
    
    class Meta:
        model = PrezzoListino
        fields= '__all__'
        
        widgets = {
            'data_inserimento': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),            
            'prezzo': forms.NumberInput(attrs={'class': 'form-control'}),            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput(),
            'fk_listino_terzista': forms.HiddenInput()
        }
        labels = {
            'data_inserimento': 'Data Inserimento',
            'prezzo': 'Prezzo',            
            'note': 'Note'

        }
        

class ListinoClienteModelForm(forms.ModelForm):
    
    
    class Meta:
        model = ListinoCliente
        fields= '__all__'
        fk_articolo = forms.ModelChoiceField(
            queryset=Articolo.objects.all(),
            label='Articolo')
        widgets = {            
            'prezzo': forms.NumberInput(attrs={'class': 'form-control'}),            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput(),
            'fk_cliente': forms.HiddenInput()
        }
        labels = {   
            'fk_articolo': 'Articolo',
            'prezzo': 'Prezzo',            
            'note': 'Note'

        }
        