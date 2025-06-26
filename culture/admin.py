# culture/admin.py

from django.contrib import admin
from django.contrib import messages
from polymorphic.admin import (
    PolymorphicInlineSupportMixin, StackedPolymorphicInline
)

# Import your new models
from .models import (
    CulturalChapter, ContentBlock, HeadingBlockOne, HeadingBlockTwo,
 HeadingBlockThree, ParagraphBlock, ImageBlock, ReferenceBlock
)

# This inline manager is the key to the admin interface.
# It tells the admin how to display forms for each type of content block.
class ContentBlockInline(StackedPolymorphicInline):

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

   
    model = ContentBlock
    child_inlines = (
        HeadingBlockOneInline,
        HeadingBlockTwoInline,
        HeadingBlockThreeInline,
        ParagraphBlockInline,
        ImageBlockInline,
        ReferenceBlockInline,
    )
    extra = 0 # Don't show any empty forms by default


# This is the main admin page for a "Cultural Chapter".
# The PolymorphicInlineSupportMixin allows it to host the inline manager above.
# The SortableAdminMixin (from django-admin-sortable2) provides drag-and-drop.
@admin.register(CulturalChapter)
class CulturalChapterAdmin(PolymorphicInlineSupportMixin, admin.ModelAdmin):
    list_display = ('name', 'district','updated_at',)
    list_filter = ('district__name', 'district__state__name')
    search_fields = ('name', 'district__name')
    prepopulated_fields = {'slug': ('name',)}

    # We add our unified ContentBlockInline here.
    # This will create a single section in the admin where you can add,
    # edit, and reorder all content blocks.
    inlines = [ContentBlockInline]
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
            f'Successfully deleted {count} cultural chapter(s) and their content blocks.',
            messages.SUCCESS
        )
    
    delete_selected_chapters.short_description = "Delete selected cultural chapters"

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