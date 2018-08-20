# Django
from django.contrib import admin

# Project
from .models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    exclude = ('data', 'data_owner', )
    search_fields = ('vin', 'model', )
    list_filter = ('year', 'make', 'data_owner')
