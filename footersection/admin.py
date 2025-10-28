from django.contrib import admin
from .models import Project, Partnership, Careers, Careers_post, Terms, Disclaimer, Message

@admin.register(Careers_post)
class CareersPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'location', 'employment_type', 'experience_level', 'is_active', 'created_at')
    list_filter = ('employment_type', 'experience_level', 'is_active', 'department', 'created_at')
    search_fields = ('title', 'department', 'location')
    list_editable = ('is_active',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'department', 'location', 'employment_type', 'experience_level')
        }),
        ('Job Details', {
            'fields': ('description', 'requirements', 'benefits')
        }),
        ('Additional Information', {
            'fields': ('salary_range', 'application_deadline', 'is_active'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject')
    list_editable = ('is_read',)
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email')
        }),
        ('Message Details', {
            'fields': ('subject', 'message')
        }),
        
    )

# Register other models
admin.site.register(Project)
admin.site.register(Partnership)
admin.site.register(Careers)
admin.site.register(Terms)
admin.site.register(Disclaimer)
