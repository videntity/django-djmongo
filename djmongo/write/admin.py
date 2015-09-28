from django.contrib import admin
from models import WriteAPI

class WriteAPIAdmin(admin.ModelAdmin):
    list_display = ('slug', 'database_name',
                    'collection_name', 'creation_date')


admin.site.register(WriteAPI, WriteAPIAdmin)
