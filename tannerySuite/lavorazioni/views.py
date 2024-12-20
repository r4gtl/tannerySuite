import datetime
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.template.loader import render_to_string
from django.http import JsonResponse


from acquistopelli.models import Lotto
from .models import *

from .forms import *

from .filters import OrdineLavoroFilter


def dashboard_lavorazioni(request):
    lavorazioni = OrdineLavoro.objects.all()

    lavorazioni_filter = OrdineLavoroFilter(request.GET, queryset=lavorazioni)

    page = request.GET.get("page", 1)
    paginator = Paginator(
        lavorazioni_filter.qs, 50
    )  # Utilizza lotti_filter.qs per la paginazione

    try:
        lavorazioni_paginator = paginator.page(page)
    except PageNotAnInteger:
        lavorazioni_paginator = paginator.page(1)
    except EmptyPage:
        lavorazioni_paginator = paginator.page(paginator.num_pages)

    context = {
        "lavorazioni_paginator": lavorazioni_paginator,
        "filter": lavorazioni_filter,
    }

    return render(request, "lavorazioni/dashboard_lavorazioni.html", context)


# Tabelle Generiche


def tabelle_generiche(request):
    causali_trasporto = CausaleTrasporto.objects.all()
    aspetto_beni = AspettoDeiBeni.objects.all()
    porti_materiale = PortoMateriale.objects.all()
    uni_misura = UnitaMisura.objects.all()

    context = {
        "causali_trasporto": causali_trasporto,
        "aspetto_beni": aspetto_beni,
        "porti_materiale": porti_materiale,
        "uni_misura": uni_misura,
    }

    return render(request, "lavorazioni/tabelle_generiche.html", context)


class CausaleTrasportoCreateView(LoginRequiredMixin, CreateView):
    model = CausaleTrasporto
    form_class = CausaleTrasportoModelForm
    template_name = "lavorazioni/generiche/causale_trasporto.html"
    success_message = "Causale di trasporto aggiunta correttamente!"
    # success_url = reverse_lazy('human_resources:human_resources')

    def get_success_url(self):
        return reverse_lazy("lavorazioni:tabelle_generiche")

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)


class CausaleTrasportoUpdateView(LoginRequiredMixin, UpdateView):
    model = CausaleTrasporto
    form_class = CausaleTrasportoModelForm
    template_name = "lavorazioni/generiche/causale_trasporto.html"
    success_message = "Causale di trasporto modificata correttamente!"
    # success_url = reverse_lazy('human_resources:human_resources')

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("lavorazioni:tabelle_generiche")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['elenco_attributi'] = DettaglioFaseLavoro.objects.filter(fk_fase_lavoro=self.object.pk)
        # context['elenco_valutazioni'] = ValutazioneOperatore.objects.filter(fk_hr=self.object.pk)
        return context


def delete_causale_trasporto(request, pk):
    deleteobject = get_object_or_404(CausaleTrasporto, pk=pk)
    deleteobject.delete()
    url_match = reverse_lazy("lavorazioni:tabelle_generiche")
    return redirect(url_match)


class AspettoDeiBeniCreateView(LoginRequiredMixin, CreateView):
    model = AspettoDeiBeni
    form_class = AspettoDeiBeniModelForm
    template_name = "lavorazioni/generiche/aspetto_beni.html"
    success_message = "Aspetto dei beni aggiunto correttamente!"
    # success_url = reverse_lazy('human_resources:human_resources')

    def get_success_url(self):
        return reverse_lazy("lavorazioni:tabelle_generiche")

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)


class AspettoDeiBeniUpdateView(LoginRequiredMixin, UpdateView):
    model = AspettoDeiBeni
    form_class = AspettoDeiBeniModelForm
    template_name = "lavorazioni/generiche/aspetto_beni.html"
    success_message = "Aspetto beni modificato correttamente!"
    # success_url = reverse_lazy('human_resources:human_resources')

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("lavorazioni:tabelle_generiche")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['elenco_attributi'] = DettaglioFaseLavoro.objects.filter(fk_fase_lavoro=self.object.pk)
        # context['elenco_valutazioni'] = ValutazioneOperatore.objects.filter(fk_hr=self.object.pk)
        return context


def delete_aspetto_beni(request, pk):
    deleteobject = get_object_or_404(AspettoDeiBeni, pk=pk)
    deleteobject.delete()
    url_match = reverse_lazy("lavorazioni:tabelle_generiche")
    return redirect(url_match)


class PortoMaterialeCreateView(LoginRequiredMixin, CreateView):
    model = PortoMateriale
    form_class = PortoMaterialeModelForm
    template_name = "lavorazioni/generiche/porto_materiale.html"
    success_message = "Porto materiale aggiunto correttamente!"
    # success_url = reverse_lazy('human_resources:human_resources')

    def get_success_url(self):
        return reverse_lazy("lavorazioni:tabelle_generiche")

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)


class PortoMaterialeUpdateView(LoginRequiredMixin, UpdateView):
    model = PortoMateriale
    form_class = PortoMaterialeModelForm
    template_name = "lavorazioni/generiche/porto_materiale.html"
    success_message = "Porto materiale modificato correttamente!"
    # success_url = reverse_lazy('human_resources:human_resources')

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("lavorazioni:tabelle_generiche")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['elenco_attributi'] = DettaglioFaseLavoro.objects.filter(fk_fase_lavoro=self.object.pk)
        # context['elenco_valutazioni'] = ValutazioneOperatore.objects.filter(fk_hr=self.object.pk)
        return context


def delete_porto_materiale(request, pk):
    deleteobject = get_object_or_404(PortoMateriale, pk=pk)
    deleteobject.delete()
    url_match = reverse_lazy("lavorazioni:tabelle_generiche")
    return redirect(url_match)


class UnitaMisuraCreateView(LoginRequiredMixin, CreateView):
    model = UnitaMisura
    form_class = UnitaMisuraModelForm
    template_name = "lavorazioni/generiche/unita_misura.html"
    success_message = "Unità di misura aggiunta correttamente!"
    # success_url = reverse_lazy('human_resources:human_resources')

    def get_success_url(self):
        return reverse_lazy("lavorazioni:tabelle_generiche")

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)


class UnitaMisuraUpdateView(LoginRequiredMixin, UpdateView):
    model = UnitaMisura
    form_class = UnitaMisuraModelForm
    template_name = "lavorazioni/generiche/unita_misura.html"
    success_message = "Unità di misura modificata correttamente!"
    # success_url = reverse_lazy('human_resources:human_resources')

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("lavorazioni:tabelle_generiche")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context['elenco_valutazioni'] = ValutazioneOperatore.objects.filter(fk_hr=self.object.pk)
        return context


def delete_unita_misura(request, pk):
    deleteobject = get_object_or_404(UnitaMisura, pk=pk)
    deleteobject.delete()
    url_match = reverse_lazy("lavorazioni:tabelle_generiche")
    return redirect(url_match)


# Fine tabelle generiche


# Ordine di Lavoro
class OrdineLavoroCreateView(LoginRequiredMixin, CreateView):
    model = OrdineLavoro
    form_class = OrdineLavoroModelForm
    template_name = "lavorazioni/ordine_lavoro.html"
    success_message = "DDT aggiunto correttamente!"
    # success_url = reverse_lazy('lavorazioni:dashboard_lavorazioni')

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)

    def get_success_url(self):
        if "salva_esci" in self.request.POST:
            return reverse_lazy("lavorazioni:dashboard_lavorazioni")

        pk_ordine_lavoro = self.object.pk
        return reverse_lazy(
            "lavorazioni:modifica_ordine_lavoro", kwargs={"pk": pk_ordine_lavoro}
        )

    def get_initial(self):
        created_by = self.request.user
        return {
            "created_by": created_by,
        }


class OrdineLavoroUpdateView(LoginRequiredMixin, UpdateView):
    model = OrdineLavoro
    form_class = OrdineLavoroModelForm
    template_name = "lavorazioni/ordine_lavoro.html"
    success_message = "Ordine lavoro modificato correttamente!"
    success_url = reverse_lazy("lavorazioni:dashboard_lavorazioni")

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)

    def get_success_url(self):
        if "salva_esci" in self.request.POST:
            return reverse_lazy("lavorazioni:dashboard_lavorazioni")

        pk_ordine_lavoro = self.object.pk
        return reverse_lazy(
            "lavorazioni:crea_ordine_lavoro", kwargs={"pk": pk_ordine_lavoro}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fk_ordine_lavoro = self.object.pk
        context["fk_ordine_lavoro"] = fk_ordine_lavoro
        context["elenco_dettagli"] = DettaglioOrdineLavoro.objects.filter(
            fk_ordine_lavoro=self.object.pk
        )
        return context


def delete_ordine_lavoro(request, pk):
    deleteobject = get_object_or_404(OrdineLavoro, pk=pk)
    deleteobject.delete()
    url_match = reverse_lazy("lavorazioni:dashboard_lavorazioni")
    return redirect(url_match)


# Dettaglio
class DettaglioOrdineLavoroCreateView(LoginRequiredMixin, CreateView):
    model = DettaglioOrdineLavoro
    form_class = DettaglioOrdineLavoroModelForm
    template_name = "lavorazioni/dettaglio_ordine_lavoro.html"
    success_message = "Dettaglio aggiunto correttamente!"

    def get_success_url(self):
        fk_ordine_lavoro = self.object.fk_ordine_lavoro.pk
        # focus_button = 'btn_new_detail'  # Imposto il pulsante su cui settare il focus

        # return reverse_lazy('ricette:modifica_dettaglio_ricetta_rifinizione_with_focus_button', kwargs={'pk':fk_ricetta_rifinizione, 'focus_button': focus_button})
        return reverse_lazy(
            "lavorazioni:modifica_ordine_lavoro", kwargs={"pk": fk_ordine_lavoro}
        )

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        ordine_lavoro_id = self.kwargs.get("fk_ordine_lavoro")
        max_numero_riga = DettaglioOrdineLavoro.objects.filter(
            fk_ordine_lavoro=ordine_lavoro_id
        ).aggregate(models.Max("numero_riga"))["numero_riga__max"]
        next_numero_riga = max_numero_riga + 1 if max_numero_riga else 1
        initial["numero_riga"] = next_numero_riga

        ordine_lavoro_id = self.kwargs.get("fk_ordine_lavoro")

        initial["fk_ordine_lavoro"] = ordine_lavoro_id
        initial["created_by"] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_ordine_lavoro = self.kwargs["fk_ordine_lavoro"]
        lotti_prova = Lotto.objects.prefetch_related("dettagliolotto_set").all()
        output_prova = OutputLavorazione.objects.prefetch_related(
            "dettagliolotto_set"
        ).all()
        elenco_dettagli_lotti = DettaglioLotto.objects.all()
        elenco_dettagli_output = OutputLavorazione.objects.all()
        context["lotti_prova"] = lotti_prova
        context["output_prova"] = output_prova
        context["elenco_dettagli_lotti"] = elenco_dettagli_lotti
        context["elenco_dettagli_output"] = elenco_dettagli_output
        context["ordine_lavoro"] = pk_ordine_lavoro
        context["dettagli_ordine_lavoro"] = get_object_or_404(
            OrdineLavoro, pk=pk_ordine_lavoro
        )
        return context


class DettaglioOrdineLavoroUpdateView(LoginRequiredMixin, UpdateView):
    model = DettaglioOrdineLavoro
    form_class = DettaglioOrdineLavoroModelForm
    template_name = "lavorazioni/dettaglio_ordine_lavoro.html"
    success_message = "Dettaglio modificato correttamente!"

    def get_success_url(self):
        fk_ordine_lavoro = self.object.fk_ordine_lavoro.pk
        return reverse_lazy(
            "lavorazioni:modifica_ordine_lavoro", kwargs={"pk": fk_ordine_lavoro}
        )

    def form_valid(self, form):
        messages.info(self.request, self.success_message)  # Compare sul success_url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_ordine_lavoro = self.kwargs["fk_ordine_lavoro"]
        context["ordine_lavoro"] = pk_ordine_lavoro
        context["dettagli_ordine_lavoro"] = get_object_or_404(
            OrdineLavoro, pk=pk_ordine_lavoro
        )
        return context


def delete_dettaglio_ordine_lavoro(request, pk):
    deleteobject = get_object_or_404(DettaglioOrdineLavoro, pk=pk)
    fk_ordine_lavoro = deleteobject.fk_ordine_lavoro.pk
    deleteobject.delete()
    url_match = reverse_lazy(
        "lavorazioni:modifica_ordine_lavoro", kwargs={"pk": fk_ordine_lavoro}
    )
    return redirect(url_match)


def ricerca_lotto(request):
    if request.method == "POST":
        form = RicercaLottoForm(request.POST)
        if form.is_valid():
            identificativo = form.cleaned_data["identificativo"]
            fornitore = form.cleaned_data["fornitore"]
            taglio = form.cleaned_data["taglio"]
            sezione = form.cleaned_data["sezione"]
            concia = form.cleaned_data["concia"]
            tipoanimale = form.cleaned_data["tipoanimale"]
            spessore = form.cleaned_data["spessore"]
            quality = form.cleaned_data["quality"]

            lotti = Lotto.objects.all()
            if identificativo:
                lotti = lotti.filter(identificativo__icontains=identificativo)
            if fornitore:
                lotti = lotti.filter(fk_fornitore=fornitore)
            if taglio:
                lotti = lotti.filter(fk_taglio=taglio)
            if sezione:
                lotti = lotti.filter(fk_sezione=sezione)
            if concia:
                lotti = lotti.filter(fk_concia=concia)
            if tipoanimale:
                lotti = lotti.filter(fk_tipoanimale=tipoanimale)
            if spessore:
                lotti = lotti.filter(spessore=spessore)
            if quality:
                lotti = lotti.filter(fk_quality=quality)

            for lotto in lotti:
                print(f"lotto: {lotto}")

            return render(
                request,
                "lavorazioni/risultati_ricerca_lotto.html",
                {"lotti": lotti, "form_ricerca": form},
            )
            # risultati_html = render_to_string('lavorazioni/risultati_ricerca_lotto.html', {'lotti': lotti})
            # return JsonResponse({'html': risultati_html})
    # return JsonResponse({'error': 'Invalid form'}, status=400)
    else:
        form = RicercaLottoForm()

    return render(request, "lavorazioni/ricerca_lotto.html", {"form_ricerca": form})


def ricerca_lotto_modal(request):
    if request.method == "GET":
        form = RicercaLottoForm()
        print("arrivato qui")
        for field in form:
            print(f"NOmecampo: {field.name}")
        return render(
            request,
            "lavorazioni/modals/modal_ricerca_lotto.html",
            {"form_ricerca": form},
        )
    else:
        # Handle potential POST requests within the modal (optional)
        return HttpResponseBadRequest()
