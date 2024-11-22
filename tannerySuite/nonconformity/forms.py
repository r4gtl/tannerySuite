from django import forms

from .models import (RapportoNC, Processo, RapportoAudit, ProcessoAudit                   
                     )





class ProcessoModelForm(forms.ModelForm):
    class Meta:
        model = Processo
        fields = '__all__'

        widgets = {
            'descrizione': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descrizione processo'}),            
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'created_by': forms.HiddenInput()
        }
        labels = {
            'descrizione': 'Descrizione processo',
            'classe_processo': 'Classe processo',            
            'note': 'Annotazioni'
        }


class RapportoNCModelForm(forms.ModelForm):

    

    class Meta:
        model = RapportoNC
        fields = '__all__'

        widgets = {
            'data_nc': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),            
            'descrizione': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrizione NC', 'rows':'3'}),
            'causa_radice': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Causa radice', 'rows':'3'}),
            'settore_responsabile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Settore responsabile'}),
            'note_decisioni_immediate': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Note decisioni immediate', 'rows':'3'}),
            'responsabile_decisione_immediata': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Responsabile'}),
            'data_limite_decisione_immediata': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),            
            'descrizione_ac': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrizione azione correttiva', 'rows':'3'}),
            'responsabile_ac': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Responsabile'}),
            'data_limite_ac': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
            'altre_decisioni_ac': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Altre decisioni', 'rows':'3'}),                        
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3', 'rows':'3'}),
            'created_by': forms.HiddenInput()
        }
        labels = {
            'numero_nc': 'Numero Rapporto',
            'data_nc': 'Data Rapporto',
            'tipo_nc': 'Tipo Rapporto',
            'compilato_da': 'Compilato da',
            'segnalato_da': 'Segnalato da',
            'fk_fornitore': 'Fornitore Non Conforme',
            'fk_cliente': 'Cliente che ha segnalato',
            'descrizione': 'Descrizione rapporto',
            'causa_radice': 'Causa radice',
            'settore_responsabile': 'Settore responsabile',
            'decisioni_immediate': 'Decisioni immediate',
            'note_decisioni_immediate': 'Note decisioni immediate',
            'responsabile_decisione_immediata': 'Responsabile decisioni immediate',
            'data_limite_decisione_immediata': 'Da terminare entro',
            'is_ac_necessaria': 'Azione correttiva Necessaria',
            'descrizione_ac': 'Descrizione Azione Correttiva',
            'responsabile_ac': 'Responsabile Azione Correttiva',
            'data_limite_ac': 'Da terminare entro',
            'is_ac_completa': 'Completata',
            'is_ac_efficace': 'Efficace',
            'altre_decisioni_ac': 'Ulteriori azioni',
            'fk_rapportoaudit': 'Rapporto di Audit Associato',
            'note': 'Annotazioni'
        }


class RapportoAuditModelForm(forms.ModelForm):

    class Meta:
        model = RapportoAudit
        fields = '__all__'
        
        widgets = {
            'data_rapporto_audit': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),            
            'norme_riferimento': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Norme di Riferimento', 'rows':'3'}),
            'auditor': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Auditors', 'rows':'3'}),            
            'risultato': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Risultato', 'rows':'3'}),
            'data_controllo': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),            
            
            'created_by': forms.HiddenInput()
        }
        labels = {
            'numero_rapporto_audit': 'Numero Rapporto',
            'data_rapporto_audit': 'Data Rapporto',
            'norme_riferimento': 'Norme di Riferimento',
            'auditor': 'Auditors',
            'risultato': 'Risultato',
            'data_controllo': 'Data Controllo',
            
        }


class ProcessoAuditModelForm(forms.ModelForm):
    class Meta:
        model = ProcessoAudit
        fields = '__all__'
        fk_processo = forms.ModelChoiceField(queryset=Processo.objects.all())
        widgets = {
            'fk_processo': forms.Select(attrs={'style':'background_color:#F5F8EC'}),
            'note': forms.Textarea(attrs={'placeholder': 'Inserisci Annotazioni', 'rows':'3'}),
            'fk_rapportoaudit': forms.HiddenInput()
        }
        labels = {
            'fk_processo': 'Processo',                       
            'note': 'Annotazioni'
        }