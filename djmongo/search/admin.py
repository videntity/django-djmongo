from django.contrib import admin
from models import SavedSearch




class SavedSearchAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('slug', 'title', 'user','creation_date')


admin.site.register(SavedSearch, SavedSearchAdmin)

