# statistic/admin.py

from django.contrib import admin
from django.contrib import messages
from polymorphic.admin import (
    PolymorphicInlineSupportMixin, StackedPolymorphicInline
)

# Import all the models from the statistic app
from .models import (
    StatisticalChapter, StatisticContentBlock, HeadingBlockOne, HeadingBlockTwo,
    HeadingBlockThree, ParagraphBlock, ImageBlock, ReferenceBlock, ChartBlock
)

# This inline manager is the key to the admin interface.
# It tells the admin how to display forms for each type of content block.
class StatisticContentBlockInline(StackedPolymorphicInline):

    # Define one inline "Child" for each of your concrete block models
    class HeadingBlockOneInline(StackedPolymorphicInline.Child):
        model = HeadingBlockOne

    class HeadingBlockTwoInline(StackedPolymorphicInline.Child):
        model = HeadingBlockTwo
    
    class HeadingBlockThreeInline(StackedPolymorphicInline.Child):
        model = HeadingBlockThree 

    class ParagraphBlockInline(StackedPolymorphicInline.Child):
        model = ParagraphBlock

    class ImageBlockInline(StackedPolymorphicInline.Child):
        model = ImageBlock

    class ReferenceBlockInline(StackedPolymorphicInline.Child):
        model = ReferenceBlock
    
    # Add the new ChartBlock so you can add charts in the admin
    class ChartBlockInline(StackedPolymorphicInline.Child):
        model = ChartBlock

    # The base model for all inlines
    model = StatisticContentBlock
    
    # List all the child inline types that can be added
    child_inlines = (
        HeadingBlockOneInline,
        HeadingBlockTwoInline,
        HeadingBlockThreeInline,
        ParagraphBlockInline,
        ImageBlockInline,
        ReferenceBlockInline,
        ChartBlockInline, # <-- Your new ChartBlock is now available!
    )
    extra = 0 # Don't show any empty forms by default
    # Note: To enable drag-and-drop ordering, you'll need to install
    # django-admin-sortable2 and add its SortableAdminMixin here.


# This is the main admin page for a "Statistical Chapter".
# The PolymorphicInlineSupportMixin allows it to host the inline manager above.
@admin.register(StatisticalChapter)
class StatisticalChapterAdmin(PolymorphicInlineSupportMixin, admin.ModelAdmin):
    list_display = ('name', 'district', 'updated_at',)
    list_filter = ('district__name', 'district__state__name')
    search_fields = ('name', 'district__name')
    # This will still work, but consider a more unique slug in your save() method
    prepopulated_fields = {'slug': ('name',)} 

    # We add our unified StatisticContentBlockInline here.
    # This creates the section where you can add, edit, and reorder all blocks.
    inlines = [StatisticContentBlockInline]
    actions = ['delete_selected_chapters']

    def get_actions(self, request):
        """Override to remove the default delete action and use our custom one"""
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def delete_selected_chapters(self, request, queryset):
        """Custom bulk delete action to handle polymorphic content blocks"""
        count = 0
        for chapter in queryset:
            # Delete content blocks first
            for block in chapter.content_blocks.all():
                block.delete()
            chapter.delete()
            count += 1
        
        self.message_user(
            request,
            f'Successfully deleted {count} statistical chapter(s) and their content blocks.',
            messages.SUCCESS
        )
    
    delete_selected_chapters.short_description = "Delete selected statistical chapters"

    def delete_model(self, request, obj):
        """Override single delete to handle polymorphic content blocks"""
        # Delete content blocks first
        for block in obj.content_blocks.all():
            block.delete()
        obj.delete()

    def delete_queryset(self, request, queryset):
        """Override bulk delete from admin interface"""
        for obj in queryset:
            # Delete content blocks first
            for block in obj.content_blocks.all():
                block.delete()
            obj.delete()

    def get_inline_instances(self, request, obj=None):
        return [inline(self.model, self.admin_site) for inline in self.inlines]