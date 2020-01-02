from django.contrib import admin
from .models import DataImport


class DataImport2Admin(admin.ModelAdmin):
    list_display = ('database_name', 'collection_name',
                    'status', 'creation_date')


admin.site.register(DataImport, DataImport2Admin)
