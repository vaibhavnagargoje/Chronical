# culture/models.py

from django.db import models
from django.utils.text import slugify
from polymorphic.models import PolymorphicModel

from django.urls import reverse

# This is the crucial link. We are importing the District model
# from your existing 'home' app.
from home.models import District

# -----------------------------------------------
# Main Chapter Model (The Page Container)
# -----------------------------------------------
class CulturalChapter(models.Model):
    """
    Represents a specific chapter (like Food, Artforms) for a District.
    This is the parent object for all content on the page.
    """
    CHAPTER_CHOICES = [
        ('Food', 'Food'),
        ('People', 'People'),
        ('Language', 'Language'),
        ('Artforms', 'Artforms'),
        ('Stories', 'Stories'),
        ('Cultural Sites', 'Cultural Sites'),
        ('Architecture', 'Architecture'),
        ('Sports & Games', 'Sports & Games'),
        ('Festivals & Fairs', 'Festivals & Fairs'),
        ('Political History', 'Political History'),
        ('Markets', 'Markets'),
        ('Local Politics', 'Local Politics'),
    ]
    # The direct relationship to your existing District model
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='cultural_chapters',null=True, blank=True)
    name = models.CharField(max_length=50, choices=CHAPTER_CHOICES)
    slug = models.SlugField(max_length=200, blank=True)

    def get_absolute_url(self):
        return reverse('culture:cultural_chapter_detail', kwargs={
            'state_slug': self.district.state.slug,
            'district_slug': self.district.slug,
            'chapter_slug': self.slug
        })
    class Meta:
        # Ensures you can only have one "Food" chapter for the "Kolhapur" district.
        unique_together = ('district', 'name')
        verbose_name = "Cultural Chapter"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.district.name}"

# -----------------------------------------------
# Polymorphic Content Blocks
# -----------------------------------------------
class ContentBlock(PolymorphicModel):
    """
    The generic, orderable base model for all content elements.
    It links to a CulturalChapter and knows its order on the page.
    """
    chapter = models.ForeignKey(CulturalChapter, on_delete=models.CASCADE, related_name='content_blocks')
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        # This is vital! It ensures all blocks are fetched in the correct order.
        ordering = ['order']

    def __str__(self):
        return f"Block #{self.order} on {self.chapter}"

# ---- Specific, concrete block types ----
# Each one inherits from ContentBlock and adds its own specific fields.

class HeadingBlockOne(ContentBlock):
    text = models.CharField(max_length=255)
    class Meta:
        verbose_name = "Heading 1"
    def __str__(self): return f"Heading: {self.text}"

class HeadingBlockTwo(ContentBlock):
    text = models.CharField(max_length=255)
    class Meta:
        verbose_name = "Heading 2"
    def __str__(self): return f"Heading: {self.text}"

class ParagraphBlock(ContentBlock):
    # This field uses the tinymce.models.HTMLField you already have
    content = models.TextField(help_text="Formatted text, lists, and tables go here.")
    class Meta:
        verbose_name = "Paragraph Block"
    def __str__(self): return f"Paragraph: {self.content[:60]}..."

class ImageBlock(ContentBlock):
    image = models.ImageField(upload_to='culture/images/')
    caption = models.CharField(max_length=255, blank=True)
    alt_text = models.CharField(max_length=255, help_text="Accessibility text for screen readers.")
    class Meta:
        verbose_name = "Image Block"
    def __str__(self): return f"Image: {self.caption or self.alt_text}"

class ReferenceBlock(ContentBlock):
    text = models.CharField(max_length=255)
    link = models.URLField(blank=True, null=True)
    class Meta:
        verbose_name = "Reference Block"
    def __str__(self): return f"Reference: {self.text}"