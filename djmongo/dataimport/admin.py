from django.contrib import admin
from .models import DataImport


class DataImportAdmin(admin.ModelAdmin):
    list_display = ('database_name', 'collection_name',
                    'status', 'creation_date')

admin.site.register(DataImport, DataImportAdmin)
