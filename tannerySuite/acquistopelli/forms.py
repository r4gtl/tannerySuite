from anagrafiche.models import Fornitore, Macello
from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from .models import (
    Lotto,
    Scelta,
    SceltaLotto,
    TipoAnimale,
    TipoGrezzo,
    Spessore,
    Quality,
    Taglio,
    Sezione,
    Concia,
    DettaglioLotto,
)


class TipoAnimaleModelForm(forms.ModelForm):
    class Meta:
        model = TipoAnimale
        fields = "__all__"

        widgets = {
            "descrizione": forms.TextInput(
                attrs={"placeholder": "Inserisci tipo animale"}
            ),
            "note": forms.Textarea(
                attrs={"placeholder": "Inserisci Annotazioni", "rows": "3"}
            ),
            "created_by": forms.HiddenInput(),
            "created_at": forms.HiddenInput(),
        }
        labels = {"descrizione": "Tipo Animale", "note": "Annotazioni"}


class TipoGrezzoModelForm(forms.ModelForm):
    class Meta:
        model = TipoGrezzo
        fields = "__all__"

        widget = {
            "descrizione": forms.TextInput(
                attrs={"placeholder": "Inserisci tipo grezzo"}
            ),
            "note": forms.Textarea(
                attrs={"placeholder": "Inserisci Annotazioni", "rows": "3"}
            ),
            "created_by": forms.HiddenInput(),
            "created_at": forms.HiddenInput(),
        }
        labels = {"descrizione": "Tipo Grezzo", "note": "Annotazioni"}


class SceltaModelForm(forms.ModelForm):
    class Meta:
        model = Scelta
        fields = "__all__"

        widget = {
            "descrizione": forms.TextInput(attrs={"placeholder": "Inserisci scelta"}),
            "note": forms.Textarea(
                attrs={"placeholder": "Inserisci Annotazioni", "rows": "3"}
            ),
            "created_by": forms.HiddenInput(),
            "created_at": forms.HiddenInput(),
        }
        labels = {"descrizione": "Scelta", "note": "Annotazioni"}


class SpessoreModelForm(forms.ModelForm):
    class Meta:
        model = Spessore
        fields = "__all__"

        widgets = {
            "descrizione": forms.TextInput(attrs={"placeholder": "Inserisci spessore"}),
            "note": forms.Textarea(
                attrs={"placeholder": "Inserisci Annotazioni", "rows": "3"}
            ),
            "created_by": forms.HiddenInput(),
            "created_at": forms.HiddenInput(),
        }
        labels = {"descrizione": "Spessore", "note": "Annotazioni"}


class QualityModelForm(forms.ModelForm):
    class Meta:
        model = Quality
        fields = "__all__"

        widgets = {
            "descrizione": forms.TextInput(attrs={"placeholder": "Inserisci qualità"}),
            "note": forms.Textarea(
                attrs={"placeholder": "Inserisci Annotazioni", "rows": "3"}
            ),
            "created_by": forms.HiddenInput(),
            "created_at": forms.HiddenInput(),
        }
        labels = {"descrizione": "Quality", "note": "Annotazioni"}


class TaglioModelForm(forms.ModelForm):
    class Meta:
        model = Taglio
        fields = "__all__"

        widgets = {
            "descrizione": forms.TextInput(attrs={"placeholder": "Inserisci taglio"}),
            "note": forms.Textarea(
                attrs={"placeholder": "Inserisci Annotazioni", "rows": "3"}
            ),
            "created_by": forms.HiddenInput(),
            "created_at": forms.HiddenInput(),
        }
        labels = {"descrizione": "Taglio", "note": "Annotazioni"}


class SezioneModelForm(forms.ModelForm):
    class Meta:
        model = Sezione
        fields = "__all__"

        widgets = {
            "descrizione": forms.TextInput(attrs={"placeholder": "Inserisci sezione"}),
            "note": forms.Textarea(
                attrs={"placeholder": "Inserisci Annotazioni", "rows": "3"}
            ),
            "created_by": forms.HiddenInput(),
            "created_at": forms.HiddenInput(),
        }
        labels = {"descrizione": "Sezione", "note": "Annotazioni"}


class ConciaModelForm(forms.ModelForm):
    class Meta:
        model = Concia
        fields = "__all__"

        widgets = {
            "descrizione": forms.TextInput(attrs={"placeholder": "Inserisci concia"}),
            "note": forms.Textarea(
                attrs={"placeholder": "Inserisci Annotazioni", "rows": "3"}
            ),
            "created_by": forms.HiddenInput(),
            "created_at": forms.HiddenInput(),
        }
        labels = {"descrizione": "Concia", "note": "Annotazioni"}


class LottoModelForm(forms.ModelForm):
    class Meta:
        model = Lotto
        fields = "__all__"
        fk_tipoanimale = forms.ModelChoiceField(queryset=TipoAnimale.objects.all())
        fk_tipogrezzo = forms.ModelChoiceField(queryset=TipoGrezzo.objects.all())
        fk_fornitore = forms.ModelChoiceField(queryset=Fornitore.objects.all())
        fk_macello = forms.ModelChoiceField(queryset=Macello.objects.all())
        origine = CountryField().formfield()
        is_lwg = forms.BooleanField(widget=forms.CheckboxInput())

        widgets = {
            "data_acquisto": forms.DateInput(
                format=("%Y-%m-%d"), attrs={"class": "form-control", "type": "date"}
            ),
            "identificativo": forms.TextInput(
                attrs={"placeholder": "Inserisci identificativo lotto"}
            ),
            "fk_fornitore": forms.Select(attrs={"style": "background_color:#F5F8EC"}),
            "fk_taglio": forms.Select(attrs={"style": "background_color:#F5F8EC"}),
            "fk_sezione": forms.Select(attrs={"style": "background_color:#F5F8EC"}),
            "fk_concia": forms.Select(attrs={"style": "background_color:#F5F8EC"}),
            "fk_tipoanimale": forms.Select(attrs={"style": "background_color:#F5F8EC"}),
            "fk_Taglio": forms.Select(attrs={"style": "background_color:#F5F8EC"}),
            "fk_spessore": forms.Select(attrs={"style": "background_color:#F5F8EC"}),
            "fk_quality": forms.Select(attrs={"style": "background_color:#F5F8EC"}),
            "origine": CountrySelectWidget(),
            "documento": forms.TextInput(
                attrs={"placeholder": "Riferimenti documento"}
            ),
            "is_lwg": forms.CheckboxInput(),
            "peso_totale": forms.NumberInput(attrs={"style": "text-align: right;"}),
            "pezzi": forms.NumberInput(
                attrs={"class": "form-control", "style": "text-align: right;"}
            ),
            "prezzo_unitario": forms.NumberInput(attrs={"style": "text-align: right;"}),
            "spese_accessorie": forms.NumberInput(
                attrs={"style": "text-align: right;"}
            ),
            "kg_km": forms.NumberInput(attrs={"style": "text-align: right;"}),
            "note": forms.Textarea(
                attrs={"placeholder": "Inserisci Annotazioni", "rows": 3}
            ),
            "created_by": forms.HiddenInput(),
            "created_at": forms.HiddenInput(),
        }
        labels = {
            "data_acquisto": "Data di Acquisto",
            "identificativo": "Identificativo",
            "fk_fornitore": "Fornitore",
            "fk_taglio": "Taglio",
            "fk_sezione": "Sezione",
            "fk_concia": "Concia",
            "fk_tipoanimale": "Tipo Animale",
            "fk_spessore": "Spessore",
            "fk_quality": "Qualità",
            "fk_macello": "Macello",
            "origine": "Origine",
            "documento": "Riferimento Documento",
            "is_lwg": "Lwg",
            "peso_totale": "Peso Netto (Kg.)",
            "pezzi": "N. Pelli",
            "prezzo_unitario": "Prezzo Unitario",
            "spese_accessorie": "Spese Accessorie",
            "kg_km": "kg*km",
            "note": "Annotazioni",
        }


class SceltaLottoModelForm(forms.ModelForm):
    class Meta:
        model = SceltaLotto
        fields = "__all__"
        # fk_lotto = forms.ModelChoiceField(queryset=Lotto.objects.all())
        fk_scelta = forms.ModelChoiceField(queryset=Scelta.objects.all())

        widget = {
            "fk_lotto": forms.HiddenInput(),
            "fk_scelta": forms.Select(attrs={"style": "background_color:#F5F8EC"}),
            "pezzi": forms.NumberInput(attrs={"class": "form-control"}),
            "note": forms.Textarea(
                attrs={"placeholder": "Inserisci Annotazioni", "rows": "3"}
            ),
            "created_by": forms.HiddenInput(),
            "created_at": forms.HiddenInput(),
        }
        labels = {"fk_scelta": "Scelta", "pezzi": "Pezzi", "note": "Annotazioni"}


class DettaglioLottoModelForm(forms.ModelForm):
    class Meta:
        model = DettaglioLotto
        fields = "__all__"

        fk_taglio = forms.ModelChoiceField(queryset=Taglio.objects.all())
        fk_sezione = forms.ModelChoiceField(queryset=Sezione.objects.all())
        fk_concia = forms.ModelChoiceField(queryset=Concia.objects.all())
        fk_tipoanimale = forms.ModelChoiceField(queryset=TipoAnimale.objects.all())
        fk_spessore = forms.ModelChoiceField(queryset=Spessore.objects.all())
        fk_quality = forms.ModelChoiceField(queryset=Quality.objects.all())

        widget = {
            "fk_lotto": forms.HiddenInput(),
            "fk_taglio": forms.Select(attrs={"style": "background_color:#F5F8EC"}),
            "fk_sezione": forms.Select(attrs={"style": "background_color:#F5F8EC"}),
            "fk_concia": forms.Select(attrs={"style": "background_color:#F5F8EC"}),
            "fk_tipoanimale": forms.Select(attrs={"style": "background_color:#F5F8EC"}),
            "fk_spessore": forms.Select(attrs={"style": "background_color:#F5F8EC"}),
            "fk_quality": forms.Select(attrs={"style": "background_color:#F5F8EC"}),
            "pezzi": forms.NumberInput(attrs={"class": "form-control"}),
            "note": forms.Textarea(
                attrs={"placeholder": "Inserisci Annotazioni", "rows": "3"}
            ),
            "created_by": forms.HiddenInput(),
            "created_at": forms.HiddenInput(),
        }
        labels = {
            "fk_taglio": "Taglio",
            "fk_sezione": "Sezione",
            "fk_concia": "Concia",
            "fk_tipoanimale": "Animale",
            "fk_spessore": "Spessore",
            "fk_quality": "Qualità",
            "pezzi": "Pezzi",
            "note": "Annotazioni",
        }
