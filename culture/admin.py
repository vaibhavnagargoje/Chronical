from django.contrib import admin
from .models import CulturalChapter, CulturalSection

class CulturalSectionInline(admin.TabularInline):
    model = CulturalSection
    extra = 1

@admin.register(CulturalChapter)
class CulturalChapterAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'slug')
    list_filter = ('district', 'name')  # Added chapter-wise filtering
    search_fields = ('name', 'district__name')  # Enable search by chapter name & district
    prepopulated_fields = {'slug': ('name',)}
    inlines = [CulturalSectionInline]
