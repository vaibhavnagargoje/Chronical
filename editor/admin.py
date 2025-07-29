from django.contrib import admin
from .models import SuggestEdit

@admin.register(SuggestEdit)
class SuggestEditAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'edit_type', 'get_chapter_title', 'status', 'created_at']
    list_filter = ['status', 'edit_type', 'app_label', 'created_at']
    search_fields = ['name', 'email', 'suggested_text', 'reason']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Submitter Information', {
            'fields': ('name', 'email', 'user', 'notify_on_review')
        }),
        ('Chapter Information', {
            'fields': ('app_label', 'chapter_id', 'section')
        }),
        ('Edit Details', {
            'fields': ('edit_type', 'current_text', 'suggested_text', 'reason', 'sources', 'supporting_file')
        }),
        ('Review Information', {
            'fields': ('status', 'reviewed_by', 'review_notes', 'created_at', 'updated_at')
        }),
    )
    
    def get_chapter_title(self, obj):
        return obj.get_chapter_title()
    get_chapter_title.short_description = 'Chapter'
