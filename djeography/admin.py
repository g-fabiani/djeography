from typing import Any

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from leaflet.admin import LeafletGeoAdminMixin

from .models import Address, Category, Contact, Entity, Report

# Register your models here.


class AddressInline(LeafletGeoAdminMixin, admin.StackedInline):
    model = Address
    extra = 1

class ContactInline(admin.TabularInline):
    model = Contact
    extra = 0


class ReportInline(admin.StackedInline):
    model = Report
    extra = 0

@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    model = Entity

    change_form_template = 'map/change_form.html'

    # List view
    list_display = ["title", "category", "evaluation", "published"]
    list_filter = ["category", "published", "evaluation"]
    search_fields = ["title", "address__city"]
    actions = ["publish", "unpublish"]

    # Detail view
    fields = ["category", ("title", "evaluation"), "description"]

    inlines = [
        AddressInline,
        ContactInline,
        ReportInline,
    ]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return self.model.objects.all()

    @admin.action(description="Pubblica le segnalazioni selezionate")
    def publish(self, request, queryset):
        queryset.update(published=True)

    @admin.action(description="Nascondi le segnalazioni selezionate")
    def unpublish(self, request, queryset):
        queryset.update(published=False)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    exclude = ["slug"]
