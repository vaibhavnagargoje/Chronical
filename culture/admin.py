from django.contrib import admin
from django.utils.html import format_html
from .models import (
    CulturalChapter, CulturalSection,
    Heading, Subheading, Text,
    Image, Reference
)

# -----------------------------------------------
# Inline Admin Classes
# -----------------------------------------------
class HeadingInline(admin.TabularInline):
    model = Heading
    extra = 1


class SubheadingInline(admin.TabularInline):
    model = Subheading
    extra = 0


class TextInline(admin.TabularInline):
    model = Text
    extra = 1


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" height="auto" />', obj.image.url)
        return "No Image"

    image_preview.short_description = 'Preview'





class ReferenceInline(admin.TabularInline):
    model = Reference
    extra = 0


# -----------------------------------------------
# ModelAdmin Classes
# -----------------------------------------------
@admin.register(CulturalChapter)
class CulturalChapterAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'cityname', 'slug')
    list_filter = ('district', 'name')
    search_fields = ('name', 'district__name', 'cityname')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(CulturalSection)
class CulturalSectionAdmin(admin.ModelAdmin):
    list_display = ('chapter', 'order')
    list_filter = ('chapter',)
    search_fields = ('chapter__name',)
    inlines = [
        HeadingInline, SubheadingInline, TextInline,
        ImageInline, ReferenceInline
    ]












