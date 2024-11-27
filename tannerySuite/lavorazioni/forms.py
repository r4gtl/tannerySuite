from django import forms

from .models import *


class AspettoDeiBeniModelForm(forms.ModelForm):
    class Meta:
        model = AspettoDeiBeni
        fields = '__all__'
        widgets = {
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci aspetto dei beni'}),              
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput()
        }
        labels = {
            'descrizione': 'Aspetto dei beni',            
            'note': 'Note'            
        }
        
class PortoMaterialeModelForm(forms.ModelForm):
    class Meta:
        model = PortoMateriale
        fields = '__all__'
        widgets = {
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci porto materiale'}),              
            'descrizione_inglese': forms.TextInput(attrs={'placeholder': 'Inserisci porto materiale'}),              
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput()
        }
        labels = {
            'descrizione': 'Porto materiale',            
            'descrizione_inglese': 'Porto materiale in inglese',            
            'note': 'Note'            
        }


class CausaleTrasportoModelForm(forms.ModelForm):
    class Meta:
        model = CausaleTrasporto
        fields = '__all__'
        widgets = {
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci causale trasporto'}),              
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput()
        }
        labels = {
            'descrizione': 'Causale trasporto',            
            'note': 'Note'            
        }
        
class UnitaMisuraModelForm(forms.ModelForm):
    class Meta:
        model = UnitaMisura
        fields = '__all__'
        widgets = {
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci unità di misura'}),              
            'abbreviazione': forms.TextInput(attrs={'placeholder': 'Inserisci abbreviazione'}),              
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput()
        }
        labels = {
            'descrizione': 'Unità di misura',            
            'abbreviazione': 'Abbreviazione',            
            'note': 'Note'            
        }
        

class OrdineLavoroModelForm(forms.ModelForm):
    int_est = forms.ChoiceField(choices=OrdineLavoro.CHOICES_INT_EST, label='Interno/Esterno')
    trasporto = forms.ChoiceField(choices=OrdineLavoro.CHOICES_TRASPORTO, widget=forms.RadioSelect, label='')
    fk_fornitore = forms.ModelChoiceField(
        queryset=Fornitore.objects.all(),
        label='Fornitore'
    )
    fk_vettore = forms.ModelChoiceField(
        queryset=Fornitore.objects.all(),
        label='Vettore'
    )
    fk_destinazione_diversa = forms.ModelChoiceField(
        queryset=DestinazioneDiversaFornitore.objects.all(),
        label='Destinazione Diversa'
    )
    fk_causale_trasporto = forms.ModelChoiceField(
        queryset=CausaleTrasporto.objects.all(),
        label='Causale Trasporto'
    )
    fk_aspetto_beni = forms.ModelChoiceField(
        queryset=AspettoDeiBeni.objects.all(),
        label='Aspetto dei Beni'
    )
    class Meta:
        model = OrdineLavoro
        #exclude=()
        fields='__all__'
        
        
        widgets = {'num_doc': forms.NumberInput(),
                'data_doc': forms.DateInput(),
                'data_inizio_trasporto': forms.DateInput(),
                'ora_inizio_trasporto': forms.TimeInput(attrs={
                    'type': 'time',
                    'class': 'form-control',  # Aggiunge classi CSS
                    'placeholder': 'HH:MM',   # Aggiunge un placeholder
                    }),
                'n_colli': forms.NumberInput(attrs={'class': 'form-control',
                    'placeholder': 'Inserisci quantità',
                    'min': 0,  
                    }),
                'peso_kg': forms.NumberInput(attrs={'class': 'form-control',
                    'placeholder': 'Inserisci quantità',
                    'min': 0,  
                    }),
                'note': forms.Textarea(attrs={
                    'class': 'form-control',
                    'placeholder': 'Inserisci note',
                }),
                'created_by': forms.HiddenInput(),  
                'created_at': forms.HiddenInput(),              
                }
        labels = {
            'num_doc': 'Numero Documento',
            'data_doc': 'Data Documento',
            'data_inizio_trasporto': 'Data inizio trasporto',    
            'ora_inizio_trasporto': 'Ora inizio trasporto',        
            'n_colli': 'Numero colli',
            'peso_kg': 'Peso',
            'note': 'Note'
        }


class DettaglioOrdineLavoroModelForm(forms.ModelForm):
    
    fk_dettaglio_lotto = forms.ModelChoiceField(
        queryset=DettaglioLotto.objects.all(),
        label='Dettaglio Lotto',
        required=False
    )
    fk_output_lavorazione = forms.ModelChoiceField(
        queryset=OutputLavorazione.objects.all(),
        label='Già lavorati',
        required=False
    )
    fk_lavorazione = forms.ModelChoiceField(
        queryset=Lavorazione.objects.all(),
        label='Lavorazione'
    )
    fk_unita_misura = forms.ModelChoiceField(
        queryset=UnitaMisura.objects.all(),
        label='Unità di Misura'
    )
    
    class Meta:
        model = DettaglioOrdineLavoro
        #exclude=()
        fields='__all__'
        
        
        widgets = {'quantity': forms.NumberInput(),
                'numero_riga': forms.NumberInput(attrs={'class': 'form-control text-end', 'readonly': 'True'}),
                'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci unità di misura'}),
                'note': forms.Textarea(attrs={
                    'class': 'form-control',
                    'placeholder': 'Inserisci note',
                }),
                'created_by': forms.HiddenInput(),
                'fk_ordine_lavoro': forms.HiddenInput()                              
                }
        labels = {
            'quantity': 'Quantità', 
            'numero_riga': 'Numero riga',
            'descrizione': 'Descrizione',
            'note': 'Note'
        }
        