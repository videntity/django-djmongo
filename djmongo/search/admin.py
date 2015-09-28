from django.contrib import admin
from models import SavedSearch, DatabaseAccessControl, Aggregation

class AggregationAdmin(admin.ModelAdmin):
    list_display = ('slug', 'user','database_name',
                    'collection_name', 'output_collection_name', 'creation_date')


admin.site.register(Aggregation, AggregationAdmin)


class SavedSearchAdmin(admin.ModelAdmin):
    list_display = ('slug', 'collection_name', 'database_name', 'user',
                    'collection_name', 'is_public', 'creation_date')


admin.site.register(SavedSearch, SavedSearchAdmin)

class DatabaseAccessControlAdmin(admin.ModelAdmin):
    list_display = ('collection_name', 'database_name', 'is_public')
admin.site.register(DatabaseAccessControl, DatabaseAccessControlAdmin)
