from django import forms

from .models import Lavorazione


class LavorazioneModelForm(forms.ModelForm):
    class Meta:
        model = Lavorazione
        fields = '__all__'


        widgets = {
            'descrizione': forms.TextInput(attrs={'placeholder': 'Inserisci descrizione lavorazione'}),            
            'codice': forms.TextInput(attrs={'placeholder': 'Inserisci codice lavorazione'}),            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput(),
            'created_at': forms.HiddenInput()
        }
        labels = {
            'descrizione': 'Descrizione',
            'codice': 'Codice',
            'note': 'Annotazioni'
        }