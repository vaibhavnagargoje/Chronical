
from django.contrib import admin
from .models import State

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


from django.contrib import admin

admin.site.site_header = "Chronical Admin"
admin.site.site_title = "Chronical Admin"
admin.site.index_title = "Chronical Admin"



from django.utils.html import format_html
from . import models

class DistrictParagraphInline(admin.StackedInline):
    model = models.DistrictParagraph
    extra = 0
    verbose_name = "Introduction Paragraph"
    verbose_name_plural = "Introduction Paragraphs"

class DistrictImageInline(admin.TabularInline):
    model = models.DistrictImage
    extra = 1
    fields = ('image', 'caption', 'alt_text', 'preview')
    readonly_fields = ('preview',)
    
    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" height="auto" />', obj.image.url)
        return "No image"
    
    preview.short_description = 'Image Preview'

class DistrictQuickFactInline(admin.TabularInline):
    model = models.DistrictQuickFact
    extra = 1


class SectionParagraphInline(admin.StackedInline):
    model = models.SectionParagraph
    extra = 1

class SectionImageInline(admin.TabularInline):
    model = models.SectionImage
    extra = 1
    fields = ('image', 'caption', 'alt_text', 'preview')
    readonly_fields = ('preview',)
    
    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" height="auto" />', obj.image.url)
        return "No image"
    
    preview.short_description = 'Image Preview'

@admin.register(models.DistrictSection)
class DistrictSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'section_type', 'district',)
    list_filter = ('section_type', 'district__state', 'district')
    search_fields = ('title', 'district__name')
    inlines = [SectionParagraphInline, SectionImageInline]
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }


@admin.register(models.District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'slug')
    list_filter = ('state',)
    search_fields = ('name', 'state__name')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [
        DistrictParagraphInline,
        DistrictImageInline,
        DistrictQuickFactInline,
    ]
    
    fieldsets = (
        (None, {
            'fields': ('state', 'name', 'slug')
        }),
        ('Introduction', {
            'fields': ('introduction',),
            'description': 'Basic introduction paragraph. You can add more paragraphs using the section below.'
        }),
    )
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/custom_admin.js',)

