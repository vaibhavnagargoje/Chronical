# culture/admin.py

from django.contrib import admin
from polymorphic.admin import (
    PolymorphicInlineSupportMixin, StackedPolymorphicInline
)
# Import your new models
from .models import (
    CulturalChapter, ContentBlock, HeadingBlockOne, HeadingBlockTwo,
    ParagraphBlock, ImageBlock, ReferenceBlock
)

# This inline manager is the key to the admin interface.
# It tells the admin how to display forms for each type of content block.
class ContentBlockInline(StackedPolymorphicInline):

    class HeadingBlockOneInline(StackedPolymorphicInline.Child):
        model = HeadingBlockOne
    class HeadingBlockTwoInline(StackedPolymorphicInline.Child):
        model = HeadingBlockTwo

    class ParagraphBlockInline(StackedPolymorphicInline.Child):
        model = ParagraphBlock

    class ImageBlockInline(StackedPolymorphicInline.Child):
        model = ImageBlock

    class ReferenceBlockInline(StackedPolymorphicInline.Child):
        model = ReferenceBlock

    # Define the parent model and the available child types
    model = ContentBlock
    child_inlines = (
        HeadingBlockOneInline,
        HeadingBlockTwoInline,
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
    list_display = ('name', 'district')
    list_filter = ('district__name', 'district__state__name')
    search_fields = ('name', 'district__name')
    prepopulated_fields = {'slug': ('name',)}

    # We add our unified ContentBlockInline here.
    # This will create a single section in the admin where you can add,
    # edit, and reorder all content blocks.
    inlines = [ContentBlockInline]

    def get_inline_instances(self, request, obj=None):
        return [inline(self.model, self.admin_site) for inline in self.inlines]