from django.contrib import admin
from models import DataImport


class DataImportAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'status','creation_date')
    
admin.site.register(DataImport, DataImportAdmin)