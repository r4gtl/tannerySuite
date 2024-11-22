from acquistopelli.models import TipoAnimale, TipoGrezzo
from django import forms

from .models import *


class ArticoloModelForm(forms.ModelForm):
    class Meta:
        model = Articolo
        fields = '__all__'
        fk_tipoanimale = forms.ModelChoiceField(queryset=TipoAnimale.objects.all())
        fk_tipogrezzo = forms.ModelChoiceField(queryset=TipoGrezzo.objects.all())
        widgets = {
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci Nome Articolo'}),            
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput()
        }
        labels = {
            'descrizione': 'Articolo',
            'fk_tipoanimale': 'Tipo Animale',
            'fk_tipogrezzo': 'Tipo Grezzo',
            'industries_served': 'Industries Served'
            
        }
        
class ColoreModelForm(forms.ModelForm):
    class Meta:
        model = Colore
        fields = '__all__'
        widgets = {
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci Nome colore'}),            
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput()
        }
        labels = {
            'descrizione': 'Colore',
            
        }

class LavorazioneEsternaModelForm(forms.ModelForm):
    class Meta:
        model = LavorazioneEsterna
        fields = '__all__'
        widgets = {
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci Nome Lavorazione'}),  
            'codice': forms.TextInput(attrs={'placeholder': 'Inserisci Codice Lavorazione'}),      
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput()
        }
        labels = {
            'descrizione': 'Fase di Lavoro',
            'codice': 'Codice Lavorazione',
            'note': 'Note'            
        }


class FaseLavoroModelForm(forms.ModelForm):
    class Meta:
        model = FaseLavoro
        fields = '__all__'
        widgets = {
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci Nome Fase'}),            
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput()
        }
        labels = {
            'descrizione': 'Fase di Lavoro',
            'interno_esterno': 'Interno/Esterno'
            
        }

class DettaglioFaseLavoroModelForm(forms.ModelForm):
    class Meta:
        model = DettaglioFaseLavoro
        fields = '__all__'
        widgets = {
            'attributo': forms.TextInput(attrs={'placeholder': 'Inserisci attributo fase (Temperatura, Codice,...)'}),            
            'fk_fase_lavoro': forms.HiddenInput(),
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput()
        }
        labels = {
            'attributo': 'Attributo',
            'note': 'Note'
            
        }


class ElencoTestModelForm(forms.ModelForm):
    class Meta:
        model = ElencoTest
        fields = '__all__'
        widgets = {
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci Nome Test'}),   
            'norma_riferimento': forms.TextInput(attrs={'placeholder': 'Inserisci norma di riferimento'}),
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput()
        }
        labels = {
            'descrizione': 'Test',
            'norma_riferimento': 'Norma di Riferimento',
            
        }

class TestArticoloModelForm(forms.ModelForm):
    class Meta:
        model = TestArticolo
        fields = '__all__'
        
        fk_test = forms.ModelChoiceField(queryset=ElencoTest.objects.all())
        widgets = {

            'valore': forms.TextInput(attrs={'placeholder': 'Inserisci valore'}), 

            'fk_articolo': forms.HiddenInput(), 
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput()
        }
        labels = {
            'valore': 'Valore',
            'fk_test': 'Test',
            'note': 'Note',
            'interno_esterno': 'Interno/Esterno'
            
        }
        


class ProceduraModelForm(forms.ModelForm):
    class Meta:
        model = Procedura
        fields = '__all__'
        
        
        widgets = {

            'nr_procedura': forms.NumberInput(attrs={'class': 'form-control text-end', 'readonly': 'True'}),
            'data_procedura': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control text-end', 'type': 'date'}),            
            'nr_revisione': forms.NumberInput(attrs={'class': 'form-control text-end', 'readonly': 'True'}),
            'data_revisione': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control text-end', 'type': 'date'}),            
            'fk_articolo': forms.HiddenInput(), 
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput()
        }
        labels = {
            'nr_procedura': 'N. Procedura',
            'data_procedura': 'Data procedura',
            'nr_revisione': 'N. Revisione',
            'data_revisione': 'Data Revisione',
            'note': 'Note',
            
            
        }
        
        

class DettaglioProceduraModelForm(forms.ModelForm):
    class Meta:
        model = DettaglioProcedura
        fields = '__all__'
        fk_faselavoro = forms.ModelChoiceField(
            queryset=FaseLavoro.objects.all(),            
            widget=forms.Select
            )
        
        widgets = {
            'numero_riga': forms.HiddenInput(), 
            'fk_procedura': forms.HiddenInput(), 
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput()
        }
        labels = {
            'fk_faselavoro': 'Fase di Lavoro',
            'fk_fornitore': 'Terzista',            
            'is_interna': 'Interna',
            'note': 'Note'
            
            
            
        }


class CaratteristicaProceduraModelForm(forms.ModelForm):
    class Meta:
        model = CaratteristicaProcedura
        fields = '__all__'        
        fk_fornitore = forms.ModelChoiceField(
            queryset=Fornitore.objects.all(),            
            widget=forms.Select
            )
        fk_dettaglio_fase_lavoro = forms.ModelChoiceField(
            queryset=DettaglioFaseLavoro.objects.all(),            
            widget=forms.Select
            )
        fk_lavorazione_esterna = forms.ModelChoiceField(
            queryset=LavorazioneEsterna.objects.all(),            
            widget=forms.Select
            )

        
        widgets = {
            'valore': forms.TextInput(attrs={'placeholder': 'Inserisci valore'}), 
            'fk_dettaglio_procedura': forms.HiddenInput(), 
            'numero_riga': forms.HiddenInput(), 
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput()
        }
        labels = {
            'fk_fornitore': 'Terzista',
            'fk_dettaglio_fase_lavoro': 'Attributo',            
            'fk_lavorazione_esterna': 'Lavorazione esterna',
            'valore': 'Valore',
            'note': 'Note'
            
            
            
        }