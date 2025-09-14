# sidepanel/admin.py

from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from .models import SidePanelTerm, ContextualDefinition

class ContextualDefinitionInline(admin.TabularInline):
    """
    Allows editing chapter-specific overrides directly from the SidePanelTerm admin page.
    Optimized for performance with many entries.
    """
    model = ContextualDefinition
    extra = 0  # Don't show extra empty forms by default
    fields = ('cultural_chapter', 'statistical_chapter', 'override_definition', 'is_active')
    verbose_name = "Chapter Specific Override"
    verbose_name_plural = "Chapter Specific Overrides"
    
    # Show only a few inlines to avoid performance issues
    max_num = 5
    show_change_link = True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ["cultural_chapter", "statistical_chapter"]:
            kwargs["queryset"] = db_field.related_model.objects.select_related('district__state')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(SidePanelTerm)
class SidePanelTermAdmin(admin.ModelAdmin):
    """Enhanced admin for managing thousands of terms efficiently"""
    list_display = ('term', 'truncated_definition', 'overrides_count', 'created_info')
    search_fields = ('term', 'default_definition')
    inlines = [ContextualDefinitionInline]
    
    # Pagination settings for better performance
    list_per_page = 50
    list_max_show_all = 200
    
    # Actions for bulk operations
    actions = ['duplicate_terms', 'export_terms']
    
    def get_queryset(self, request):
        """Optimize queryset for better performance"""
        return super().get_queryset(request).annotate(
            overrides_count=Count('contextual_definitions')
        )
    
    def truncated_definition(self, obj):
        """Show truncated definition for better table display"""
        if len(obj.default_definition) > 100:
            return format_html(
                '<span title="{}">{}</span>',
                obj.default_definition,
                obj.default_definition[:100] + '...'
            )
        return obj.default_definition
    truncated_definition.short_description = 'Definition'
    
    def overrides_count(self, obj):
        """Show number of overrides with color coding"""
        count = obj.overrides_count
        if count == 0:
            color = 'gray'
        elif count <= 3:
            color = 'green'
        elif count <= 10:
            color = 'orange'
        else:
            color = 'red'
            
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            count
        )
    overrides_count.short_description = 'Overrides'
    overrides_count.admin_order_field = 'overrides_count'
    
    def created_info(self, obj):
        """Show creation info"""
        return format_html(
            '<small>ID: {}</small>',
            obj.id
        )
    created_info.short_description = 'Info'
    
    def duplicate_terms(self, request, queryset):
        """Bulk action to duplicate terms"""
        count = 0
        for term in queryset:
            new_term = SidePanelTerm.objects.create(
                term=f"{term.term} (Copy)",
                default_definition=term.default_definition
            )
            count += 1
        
        self.message_user(request, f"Successfully duplicated {count} terms.")
    duplicate_terms.short_description = "Duplicate selected terms"
    
    def export_terms(self, request, queryset):
        """Export terms to CSV (simplified)"""
        # This would typically generate a CSV download
        count = queryset.count()
        self.message_user(request, f"Would export {count} terms to CSV.")
    export_terms.short_description = "Export selected terms"

@admin.register(ContextualDefinition)
class ContextualDefinitionAdmin(admin.ModelAdmin):
    """
    Enhanced admin for managing thousands of overrides efficiently.
    Provides advanced filtering and search capabilities.
    """
    list_display = ('term_link', 'chapter_info', 'status_badge', 'definition_preview', 'action_links')
    list_filter = (
        'is_active', 
        'cultural_chapter__district__state',
        'statistical_chapter__district__state',
        'cultural_chapter__district',
        'statistical_chapter__district'
    )
    search_fields = (
        'term__term', 
        'cultural_chapter__name', 
        'statistical_chapter__name',
        'override_definition'
    )
    
    # Optimize for large datasets
    list_per_page = 25
    list_max_show_all = 100
    
    # Use autocomplete for better performance
    autocomplete_fields = ['term', 'cultural_chapter', 'statistical_chapter']
    
    # Bulk actions
    actions = ['activate_overrides', 'deactivate_overrides', 'bulk_delete_overrides']
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related(
            'term',
            'cultural_chapter__district__state',
            'statistical_chapter__district__state'
        )
    
    def term_link(self, obj):
        """Link to the term's admin page"""
        url = f"/admin/sidepanal/sidepanelterm/{obj.term.id}/change/"
        return format_html('<a href="{}">{}</a>', url, obj.term.term)
    term_link.short_description = 'Term'
    term_link.admin_order_field = 'term__term'
    
    def chapter_info(self, obj):
        """Display chapter information compactly"""
        chapter = obj.cultural_chapter or obj.statistical_chapter
        if chapter:
            chapter_type = "Cultural" if obj.cultural_chapter else "Statistical"
            district_info = ""
            if hasattr(chapter, 'district') and chapter.district:
                district_info = f" ({chapter.district.name})"
            
            return format_html(
                '<div><strong>{}</strong><br><small>{}{}</small></div>',
                chapter.name[:30] + ('...' if len(chapter.name) > 30 else ''),
                chapter_type,
                district_info
            )
        return "No Chapter"
    chapter_info.short_description = 'Chapter'
    
    def status_badge(self, obj):
        """Show status with color badge"""
        if obj.is_active:
            return format_html(
                '<span style="background: #28a745; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">ACTIVE</span>'
            )
        else:
            return format_html(
                '<span style="background: #dc3545; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">INACTIVE</span>'
            )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'is_active'
    
    def definition_preview(self, obj):
        """Show definition preview"""
        if obj.override_definition:
            preview = obj.override_definition[:50] + ('...' if len(obj.override_definition) > 50 else '')
            return format_html('<span title="{}">{}</span>', obj.override_definition, preview)
        else:
            return format_html('<em style="color: #6c757d;">Uses default definition</em>')
    definition_preview.short_description = 'Definition'
    
    def action_links(self, obj):
        """Quick action links"""
        return format_html(
            '<a href="/admin/sidepanal/contextualdefinition/{}/change/" style="margin-right: 5px;">Edit</a>'
            '<a href="/admin/sidepanal/contextualdefinition/{}/delete/" style="color: #dc3545;">Delete</a>',
            obj.id, obj.id
        )
    action_links.short_description = 'Actions'
    
    def activate_overrides(self, request, queryset):
        """Bulk activate overrides"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f"Successfully activated {updated} overrides.")
    activate_overrides.short_description = "Activate selected overrides"
    
    def deactivate_overrides(self, request, queryset):
        """Bulk deactivate overrides"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f"Successfully deactivated {updated} overrides.")
    deactivate_overrides.short_description = "Deactivate selected overrides"
    
    def bulk_delete_overrides(self, request, queryset):
        """Bulk delete overrides"""
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"Successfully deleted {count} overrides.")
    bulk_delete_overrides.short_description = "Delete selected overrides"

# Custom admin site configuration
admin.site.site_header = "Chronical Side Panel Administration"
admin.site.site_title = "Side Panel Admin"
admin.site.index_title = "Manage Side Panel Terms and Overrides"