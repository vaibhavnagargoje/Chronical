from django.contrib import admin
from .models import State,DistrictSVG
from django.utils.html import format_html
from . import models

admin.site.register(DistrictSVG)




@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


from django.contrib import admin

admin.site.site_header = "Chronical Admin"
admin.site.site_title = "Chronical Admin"
admin.site.index_title = "Chronical Admin"




class DistrictParagraphInline(admin.StackedInline):
    model = models.DistrictParagraph
    extra = 0
    verbose_name = "Introduction Paragraph"
    verbose_name_plural = "Introduction Paragraphs"

class DistrictImageInline(admin.TabularInline):
    model = models.DistrictImage
    extra = 1
    fields = ('original_image', 'caption', 'alt_text', 'preview')
    readonly_fields = ('preview',)
    
    def preview(self, obj):
        if obj.original_image and hasattr(obj, 'webp_small') and obj.webp_small:
            return format_html('<img src="{}" width="150" height="auto" />', obj.webp_small.url)
        return "Saving... image will be processed."
    
    preview.short_description = 'Image Preview'

class DistrictQuickFactInline(admin.TabularInline):
    model = models.DistrictQuickFact
    extra = 1




class GIFImageInline(admin.TabularInline):
    model = models.GIFImage
    extra = 1
    fields = ('original_file', 'caption', 'alt_text', 'preview')
    readonly_fields = ('preview','optimized_video')
    
    def preview(self, obj):
        if obj.optimized_video:
            # Show the converted video in the admin
            return format_html(
                '<video src="{}" width="200" autoplay muted loop></video>', 
                obj.optimized_video.url
            )
        elif obj.original_file:
            # Show the original GIF while it's processing
            return format_html('<img src="{}" width="150" /> <br> (Processing to video...)', obj.original_file.url)
        return "No GIF uploaded"
    
    preview.short_description = 'Gif Image Preview'



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
        GIFImageInline
        
    ]
    
    fieldsets = (
        (None, {
            'fields': ('state', 'name', 'slug',)
        }),
        ('Introduction', {
            'fields': ('introduction',),
            'description': 'Basic introduction paragraph. You can add more paragraphs using the section below.',
            'classes': ('wide',),
        }),
    )
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/custom_admin.js', 'tinymce/tinymce.min.js',)







@admin.register(models.DeveloperCheck)
class DeveloperCheckAdmin(admin.ModelAdmin):
    list_display = ('chapter_name', 'chapter_type', 'district', 'ready_for_review', 'reviewed', 'created_by', 'reviewed_by', 'updated_at')
    list_filter = ('ready_for_review', 'reviewed', 'created_by', 'reviewed_by')
    search_fields = ('cultural_chapter__name', 'statistical_chapter__name', 'cultural_chapter__district__name', 'statistical_chapter__district__name')
    readonly_fields = ('created_at', 'updated_at', 'reviewed_at', 'chapter_name', 'chapter_type', 'district')
    
    fieldsets = (
        ('Chapter Selection', {
            'fields': ('cultural_chapter', 'statistical_chapter'),
            'description': 'Select either a Cultural or Statistical chapter (not both)',
        }),
        ('Developer Review Status', {
            'fields': ('ready_for_review', 'reviewed'),
            'classes': ('wide',),
        }),
        ('User Tracking', {
            'fields': ('created_by', 'reviewed_by'),
        }),
        ('Information', {
            'fields': ('chapter_name', 'chapter_type', 'district'),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'reviewed_at'),
            'classes': ('collapse',),
        }),
    )
    
    def chapter_type(self, obj):
        if obj.cultural_chapter:
            return "Cultural"
        elif obj.statistical_chapter:
            return "Statistical"
        return "Unknown"
    chapter_type.short_description = "Chapter Type"
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        if obj.reviewed and not obj.reviewed_by:
            obj.reviewed_by = request.user
        super().save_model(request, obj, form, change)
    
    actions = ['mark_ready', 'mark_reviewed', 'mark_unreviewed']
    
    def mark_ready(self, request, queryset):
        queryset.update(ready_for_review=True)
        self.message_user(request, f"{queryset.count()} chapters marked as ready for developer review.")
    mark_ready.short_description = "Mark as ready for developer review"
    
    def mark_reviewed(self, request, queryset):
        from django.utils import timezone
        queryset.update(reviewed=True, reviewed_by=request.user, reviewed_at=timezone.now())
        self.message_user(request, f"{queryset.count()} chapters marked as developer reviewed.")
    mark_reviewed.short_description = "Mark as developer reviewed"
    
    def mark_unreviewed(self, request, queryset):
        queryset.update(reviewed=False, reviewed_by=None, reviewed_at=None)
        self.message_user(request, f"{queryset.count()} chapters marked as not developer reviewed.")
    mark_unreviewed.short_description = "Mark as not developer reviewed"



@admin.register(models.FinalCheck)
class FinalCheckAdmin(admin.ModelAdmin):
    list_display = ('chapter_name', 'chapter_type', 'district', 'ready_for_review', 'reviewed', 'created_by', 'reviewed_by', 'updated_at')
    list_filter = ('ready_for_review', 'reviewed', 'created_by', 'reviewed_by')
    search_fields = ('cultural_chapter__name', 'statistical_chapter__name', 'cultural_chapter__district__name', 'statistical_chapter__district__name')
    readonly_fields = ('created_at', 'updated_at', 'reviewed_at', 'chapter_name', 'chapter_type', 'district')
    
    fieldsets = (
        ('Chapter Selection', {
            'fields': ('cultural_chapter', 'statistical_chapter'),
            'description': 'Select either a Cultural or Statistical chapter (not both)',
        }),
        ('Final Review Status', {
            'fields': ('ready_for_review', 'reviewed'),
            'classes': ('wide',),
        }),
        ('User Tracking', {
            'fields': ('created_by', 'reviewed_by'),
        }),
        ('Information', {
            'fields': ('chapter_name', 'chapter_type', 'district'),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'reviewed_at'),
            'classes': ('collapse',),
        }),
    )
    
    def chapter_type(self, obj):
        if obj.cultural_chapter:
            return "Cultural"
        elif obj.statistical_chapter:
            return "Statistical"
        return "Unknown"
    chapter_type.short_description = "Chapter Type"
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        if obj.reviewed and not obj.reviewed_by:
            obj.reviewed_by = request.user
        super().save_model(request, obj, form, change)
    
    actions = ['mark_ready', 'mark_reviewed', 'mark_unreviewed']
    
    def mark_ready(self, request, queryset):
        queryset.update(ready_for_review=True)
        self.message_user(request, f"{queryset.count()} chapters marked as ready for final review.")
    mark_ready.short_description = "Mark as ready for final review"
    
    def mark_reviewed(self, request, queryset):
        from django.utils import timezone
        queryset.update(reviewed=True, reviewed_by=request.user, reviewed_at=timezone.now())
        self.message_user(request, f"{queryset.count()} chapters marked as final reviewed.")
    mark_reviewed.short_description = "Mark as final reviewed"
    
    def mark_unreviewed(self, request, queryset):
        queryset.update(reviewed=False, reviewed_by=None, reviewed_at=None)
        self.message_user(request, f"{queryset.count()} chapters marked as not final reviewed.")
    mark_unreviewed.short_description = "Mark as not final reviewed"


