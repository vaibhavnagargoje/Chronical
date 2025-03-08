
from django.contrib import admin
from .models import State, District

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'slug')
    list_filter = ('state',)
    prepopulated_fields = {'slug': ('name',)}


from django.contrib import admin

admin.site.site_header = "Chronical Admin"
admin.site.site_title = "Chronical Admin"
admin.site.index_title = "Chronical Admin"
