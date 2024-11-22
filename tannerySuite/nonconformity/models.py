from django.db import models
from django.contrib.auth.models import User
#from human_resources.models import HumanResource
from anagrafiche.models import Fornitore, Cliente

from django.db.models import Count




class Processo(models.Model):
    # Classe Processo
    DIREZIONALE = 'Direzionale'
    PRINCIPALE = 'Principale'
    SUPPORTO = 'Supporto'
    
    
    
    CHOICES_CLASSE_PROCESSO = (
        (DIREZIONALE, 'Direzionale'),
        (PRINCIPALE, 'Principale'),        
        (SUPPORTO, 'Supporto')
        
    )
    descrizione = models.CharField(max_length=100)
    classe_processo = models.CharField(max_length=50, choices=CHOICES_CLASSE_PROCESSO)  
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='processo_audit', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.descrizione)
    


class RapportoAudit(models.Model):
    numero_rapporto_audit = models.PositiveIntegerField(editable=False)
    data_rapporto_audit = models.DateField(null=False, blank=False)
    norme_riferimento = models.TextField(null=True, blank=True)
    auditor = models.TextField(null=True, blank=True)
    risultato = models.TextField(null=True, blank=True)
    data_controllo = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='rapporto_audit', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_rapporto_audit"]

    def save(self, *args, **kwargs):
        if not self.numero_rapporto_audit:
            last_number = RapportoAudit.objects.order_by('-numero_rapporto_audit').first()
            if last_number:
                self.numero_rapporto_audit = last_number.numero_rapporto_audit + 1
                print("Last number: " + str(last_number))
            else:
                self.numero_rapporto_audit = 1
        super().save(*args, **kwargs)




    def __str__(self):
        formatted_date = self.data_rapporto_audit.strftime('%d/%m/%Y')
        return str(self.numero_rapporto_audit) + " del " + formatted_date


class RapportoNC(models.Model):

    # TipoNC
    NC_SISTEMA = 'NC di Sistema'
    NC_PRODUZIONE = 'NC di Produzione'
    NC_CLIENTE = 'NC da Cliente'
    NC_FORNITORE = 'NC a Fornitore'
    NC_AMBIENTALE = 'NC Aspetti Ambientali'
    COMMENTO = 'Commento'
    
    
    CHOICES_TIPO_NC = (
        (NC_SISTEMA, 'NC di Sistema'),
        (NC_PRODUZIONE, 'NC di Produzione'),        
        (NC_CLIENTE, 'NC da Cliente'),
        (NC_FORNITORE, 'NC a Fornitore'),
        (NC_AMBIENTALE, 'NC Aspetti Ambientali'),
        (COMMENTO, 'Commento')
    )

    # Segnalato da
    CLIENTE = 'Cliente'
    FORNITORE = 'Fornitore'
    INTERNO = 'Interno'
      
    
    CHOICES_SEGNALATO_DA = (
        (CLIENTE, 'Cliente'),
        (FORNITORE, 'Fornitore'),        
        (INTERNO, 'Interno')
        
    )

    # Decisioni Immediate
    ACCETTARE = 'Accettare'
    RILAVORARE = 'Rilavorare'
    SCARTARE = 'Scartare'
    SOSTITUIRE = 'Sostituire'
    ALTRO = 'Altro'
      
    
    CHOICES_DECISIONI_IMMEDIATE = (
        (ACCETTARE, 'Accettare'),
        (RILAVORARE, 'Rilavorare'),        
        (SCARTARE, 'Scartare'),
        (SOSTITUIRE, 'Sostituire'),
        (ALTRO, 'Altro')
        
    )



    numero_nc = models.PositiveIntegerField(editable=False)
    data_nc = models.DateField(null=False, blank=False) 
    tipo_nc = models.CharField(max_length=50, choices=CHOICES_TIPO_NC)    
    '''compilato_da = models.ForeignKey(
        HumanResource,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={'datadimissioni__isnull': True}
    )'''
    segnalato_da = models.CharField(max_length=50, choices=CHOICES_SEGNALATO_DA)    
    fk_fornitore = models.ForeignKey(Fornitore, on_delete=models.SET_NULL, null=True, blank=True)
    fk_cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    descrizione = models.TextField(null=True, blank=True)
    causa_radice = models.TextField(null=True, blank=True)
    settore_responsabile = models.CharField(max_length=100, null=True, blank=True)
    decisioni_immediate = models.CharField(max_length=50, choices=CHOICES_DECISIONI_IMMEDIATE)  
    note_decisioni_immediate = models.TextField(null=True, blank=True)
    responsabile_decisione_immediata = models.CharField(max_length=50, null=True, blank=True)
    data_limite_decisione_immediata = models.DateField(null=True, blank=True) 
    is_ac_necessaria = models.BooleanField(default=False)
    descrizione_ac = models.TextField(null=True, blank=True)
    responsabile_ac = models.CharField(max_length=50, null=True, blank=True)
    data_limite_ac = models.DateField(null=True, blank=True) 
    is_ac_completa = models.BooleanField(default=False)
    is_ac_efficace = models.BooleanField(default=False)
    altre_decisioni_ac = models.TextField(null=True, blank=True)
    fk_rapportoaudit = models.ForeignKey(RapportoAudit, on_delete=models.CASCADE, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='rapportornc', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_nc"]


    def save(self, *args, **kwargs):
        if not self.numero_nc:
            last_number = RapportoNC.objects.order_by('-numero_nc').first()
            if last_number:
                self.numero_nc = last_number.numero_nc + 1
            else:
                self.numero_nc = 1
        super().save(*args, **kwargs)

    def __str__(self):
        formatted_date = self.data_nc.strftime('%d/%m/%Y')
        return str(self.numero_nc) + " del " + formatted_date
    
    @classmethod
    def get_data_for_chart(cls, from_date, to_date):
        # Esegue la query per ottenere il conteggio dei record per ogni tipo_nc
        data_set = (
            cls.objects
            .filter(data_nc__range=[from_date, to_date])
            .values('tipo_nc')
            .annotate(count=Count('id'))
        )
        print("Data_set: " + str(data_set))
        # Formatta i dati nel formato desiderato per il grafico
        data = [{'tipo_nc': item['tipo_nc'], 'count': item['count']} for item in data_set]
        print("Dati: " + str(data))
        return data
    

class ProcessoAudit(models.Model):
    fk_rapportoaudit = models.ForeignKey(RapportoAudit, on_delete=models.CASCADE)
    fk_processo = models.ForeignKey(Processo, on_delete=models.CASCADE)
    note = models.TextField(null=True, blank=True)


