from django.contrib import admin
from .models import SavedSearch, DatabaseAccessControl




class SavedSearchAdmin(admin.ModelAdmin):
    list_display = ('slug', 'collection_name', 'database_name', 'user',
                    'is_public', 'creation_date')


admin.site.register(SavedSearch, SavedSearchAdmin)

class DatabaseAccessControlAdmin(admin.ModelAdmin):
    list_display = ('collection_name', 'database_name', 'is_public')
admin.site.register(DatabaseAccessControl, DatabaseAccessControlAdmin)
