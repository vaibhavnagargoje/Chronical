from django.contrib import admin
from .models import StatisticalChapter, StatisticalSection

class StatisticalSectionInline(admin.TabularInline):
    model = StatisticalSection
    extra = 1

@admin.register(StatisticalChapter)
class StatisticalChapterAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'slug')
    list_filter = ('district', 'name')  # Added chapter-wise filtering
    search_fields = ('name', 'district__name')  # Enable search by chapter name & district
    prepopulated_fields = {'slug': ('name',)}
    inlines = [StatisticalSectionInline]
