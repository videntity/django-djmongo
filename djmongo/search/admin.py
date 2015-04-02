from django.contrib import admin
from models import SavedSearch, DatabaseAccessControl, Aggregation

class AggregationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('slug', 'title', 'user','creation_date')


admin.site.register(Aggregation, AggregationAdmin)


class SavedSearchAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('slug', 'title', 'user','creation_date')


admin.site.register(SavedSearch, SavedSearchAdmin)

class DatabaseAccessControlAdmin(admin.ModelAdmin):
    list_display = ('database_name', 'collection_name', 'is_public')
admin.site.register(DatabaseAccessControl, DatabaseAccessControlAdmin)
