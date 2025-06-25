# sidepanal/admin.py

from django.contrib import admin
from .models import CulturalSidePanal, StatisticalSidePanal, StatisticalSidePanelManager,CulturalSidePanelManager

# --- Part 1: The Inline for dynamic adding ---
# This defines the "add more" widget with the '+' button.

class StatisticalSidePanalInline(admin.StackedInline):
    model = StatisticalSidePanal
    fields = ('word', 'definition')
    extra = 1  # Show one empty form to start with
    verbose_name_plural = 'Add/Edit Side Panel Entries for this Chapter'
    # Adding a CSS class to visually separate this section
    classes = ['collapse']


class CulturalSidePanalInline(admin.StackedInline):
    model = CulturalSidePanal
    fields = ('word', 'definition')
    extra = 1  # Show one empty form to start with
    verbose_name_plural = 'Add/Edit Side Panel Entries for this Chapter'
    # Adding a CSS class to visually separate this section
    classes = ['collapse']


# --- Part 2: The Main Admin View for the Proxy Model ---
# This is the primary interface you will now use.

@admin.register(StatisticalSidePanelManager)
class StatisticalSidePanelManagerAdmin(admin.ModelAdmin):
    """
    This admin view lists all Statistical Chapters. When you click one,
    you can add side panel entries inline.
    """
    # The list view shows chapters you can select
    list_display = ('name', 'get_district_and_state')
    list_filter = ('district__state__name', 'district__name')
    search_fields = ('name', 'district__name')

    # This is the key: it attaches the inline "add more" widget
    inlines = [StatisticalSidePanalInline]

    # We make this page read-only for the chapter fields because you should
    # edit chapter details in the 'statistics' app, not here. This admin's
    # only purpose is to manage side panels.
    readonly_fields = ('name', 'district', 'slug')
    fields = ('name', 'district') # Only show these fields, and they'll be read-only

    @admin.display(description='District / State', ordering='district__name')
    def get_district_and_state(self, obj):
        return f"{obj.district.name}, {obj.district.state.name}"

    def has_add_permission(self, request):
        # Disable the "Add" button for this view. You don't add chapters here,
        # you just manage the side panels for existing ones.
        return False

    def has_delete_permission(self, request, obj=None):
        # Similarly, prevent deleting chapters from this interface.
        return False





@admin.register(CulturalSidePanelManager)
class CulturalSidePanelManagerAdmin(admin.ModelAdmin):
    """
    This admin view lists all Cultural Chapters. When you click one,
    you can add side panel entries inline.
    """
    # The list view shows chapters you can select
    list_display = ('name', 'get_district_and_state')
    list_filter = ('district__state__name', 'district__name')
    search_fields = ('name', 'district__name')

    # This is the key: it attaches the inline "add more" widget
    inlines = [CulturalSidePanalInline]

    # We make this page read-only for the chapter fields because you should
    # edit chapter details in the 'cultural' app, not here. This admin's
    # only purpose is to manage side panels.
    readonly_fields = ('name', 'district', 'slug')
    fields = ('name', 'district')  # Only show these fields, and they'll be read-only

    @admin.display(description='District / State', ordering='district__name')
    def get_district_and_state(self, obj):
        return f"{obj.district.name}, {obj.district.state.name}"

    def has_add_permission(self, request):
        # Disable the "Add" button for this view. You don't add chapters here,
        # you just manage the side panels for existing ones.
        return False

    def has_delete_permission(self, request, obj=None):
        # Similarly, prevent deleting chapters from this interface.
        return False














# # --- Part 3: (Optional but Recommended) Keep the original view for searching all entries ---
# # This is the admin from my previous answer. It's still very useful for
# # searching or editing a specific word across ALL chapters at once.

# @admin.register(StatisticalSidePanal)
# class StatisticalSidePanalAdmin(admin.ModelAdmin):
#     list_display = ('word', 'statistical_chapter', 'updated_at')
#     search_fields = ('word', 'definition', 'statistical_chapter__name')
#     autocomplete_fields = ['statistical_chapter']

# @admin.register(CulturalSidePanal)
# class CulturalSidePanalAdmin(admin.ModelAdmin):
#     list_display = ('word', 'cultural_chapter', 'updated_at')
#     search_fields = ('word', 'definition', 'cultural_chapter__name')
#     autocomplete_fields = ['cultural_chapter']