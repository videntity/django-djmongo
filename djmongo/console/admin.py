from django.contrib import admin
from models import CreateHistory



class CreateHistoryAdmin(admin.ModelAdmin):
    list_display = ('database_name', 'collection_name', 'history')
admin.site.register(CreateHistory, CreateHistoryAdmin)


