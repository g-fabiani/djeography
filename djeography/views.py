from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, F, Max, Prefetch, Q
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.generic import DetailView, ListView, TemplateView, View
from djgeojson.views import GeoJSONLayerView

from djeography import app_settings

from .models import Address, Category, Entity, EvaluationLevel, Report


class EntityListView(ListView):
    """
    Vista per tutte le segnalazioni.

    Le segnalazioni possono essere filtrate per categoria e provincia.
    È inoltre possibile compiere ricerche sulle segnalazioni.
    """

    model = Entity
    template_name = 'map/list.html'
    context_object_name = 'entities'
    paginate_by = app_settings['PAGINATION']

    def get_queryset(self) -> QuerySet[Any]:
        # Solo gli utenti autenticati possono vedere segnalazioni
        # non pubblicate
        if self.request.user.is_authenticated:
            queryset = super().get_queryset()
        else:
            queryset = self.model.published_objects.all()

        # Filtri e ricerca
        province_filter = self.request.GET.get('province')
        category_filter = self.request.GET.get('category')
        evaluation_filter = self.request.GET.get('evaluation')
        search = self.request.GET.get('search')

        self.searching = any(
            (province_filter, category_filter, evaluation_filter, search),
        )

        if search:
            # Vedi https://docs.djangoproject.com/en/5.2/topics/db/search/
            # per documentazione sulle funzioni di ricerca
            queryset = queryset.filter(
                Q(address__city__icontains=search) | Q(title__icontains=search),
            )

        else:
            # Applica i filtri solo se non sta svolgendo una ricerca
            if province_filter:
                queryset = queryset.filter(address__province=province_filter)
            if category_filter:
                queryset = queryset.filter(category__slug=category_filter)
            if evaluation_filter:
                queryset = queryset.filter(evaluation=evaluation_filter)

        # Aggiungi numero di testimonianze e testimonianza più recente
        queryset = queryset.annotate(
            latest_update=Max('report__date_added'),
            n_reports=Count('report', distinct=True),
        )

        return queryset.order_by(
            'published', F('latest_update').desc(nulls_last=True), 'id'
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        # Dati per la creazione del form
        context['provinces'] = dict(app_settings['PROV_CHOICES'])
        context['categories'] = {cat.slug: cat for cat in Category.objects.all()}
        context['evaluations'] = {
            level.short_name: level.full_name for level in EvaluationLevel.objects.all()
        }
        context['searching'] = self.searching

        return context


class EntityDetailView(DetailView):
    """Vista per una singola segnalazione e le testimonianze pertinenti a quella segnalazione."""

    model = Entity
    template_name = 'map/detail.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context['title'] = self.object.title

        return context

    def get_queryset(self) -> QuerySet[Any]:
        # Solo gli utenti autenticati possono vedere le segnalazioni
        # non pubblicate
        if self.request.user.is_authenticated:
            queryset = super().get_queryset()
        else:
            queryset = self.model.published_objects.all()
        return queryset.prefetch_related(
            Prefetch('report_set', queryset=Report.objects.order_by('-date_added')),
        )


class EntityPublishView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        entity = get_object_or_404(Entity, pk=pk)
        entity.publish()
        messages.add_message(
            request,
            messages.SUCCESS,
            f'Hai reso pubblica la segnalazione {entity.title} ({entity.category})',
        )
        return HttpResponseRedirect(entity.get_absolute_url())


class EntityUnpublishView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        entity = get_object_or_404(Entity, pk=pk)
        entity.unpublish()
        messages.add_message(
            request,
            messages.WARNING,
            f'Hai nascosto la segnalazione {entity.title} ({entity.category})',
        )
        return HttpResponseRedirect(entity.get_absolute_url())


class GeoJSONLayerByCategoryView(GeoJSONLayerView):
    model = Address
    properties = ('evaluation', 'published', 'popupUrl')
    geometry_field = 'coords'

    def get_queryset(self, **kwargs):
        queryset = self.model.objects.filter(
            entity__category__slug=self.kwargs['slug'],
        ).annotate(evaluation=F('entity__evaluation'), published=F('entity__published'))
        if not self.request.user.is_authenticated:
            return queryset.filter(entity__published=True)
        return queryset


class MapView(TemplateView):
    template_name = 'map/map.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = [
            {'name': cat.name, 'icon': cat.icon, 'url': cat.url}
            for cat in Category.objects.all()
        ]
        context['color_map'] = dict(
            {level.short_name: level.color for level in EvaluationLevel.objects.all()},
            default=app_settings.get('DEFAULT_MARKER_COLOR'),
        )
        return context

    @xframe_options_sameorigin
    def render_to_response(self, context, **response_kwargs):
        """Allow the view to be embedded in pages of the same site."""
        return super().render_to_response(context, **response_kwargs)


class PopupView(DetailView):
    model = Address
    template_name = 'map/popup.html'

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related(
                'entity__category',
            )
            .annotate(
                entity_latest_update=Max('entity__report__date_added'),
                entity_n_reports=Count('entity__report'),
            )
        )
