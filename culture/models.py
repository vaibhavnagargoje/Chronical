# culture/models.py

from django.db import models
from django.utils.text import slugify
from polymorphic.models import PolymorphicModel
from tinymce.models import HTMLField
from django.urls import reverse
import os
import uuid
from home.models import District

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from django.core.validators import FileExtensionValidator

def get_seo_image_path(instance, filename):
    """
    Generates a unique, SEO-friendly path for an uploaded image.
    Example: culture/images/mango-image-for-boy-a1b2c3d4.jpg
    """
    # 1. Start with a fallback name in case the caption is empty
    base_name = uuid.uuid4().hex

    # 2. Use the caption to create a clean, URL-friendly slug
    # We check the instance's caption first, as it's the most descriptive.
    if instance.caption:
        base_name = slugify(instance.caption)
   
    elif instance.alt_text:
        base_name = slugify(instance.alt_text)
    
   
    ext = os.path.splitext(filename)[1]


    unique_id = uuid.uuid4().hex[:8]
    new_filename = f"{base_name}-{unique_id}{ext}"

    state_slug = instance.chapter.district.state.slug if instance.chapter.district.state else 'unknown-state'
    district_slug = instance.chapter.district.slug if instance.chapter.district else 'unknown-district'
    chapter_slug = instance.chapter.slug 

    return os.path.join('culture', 'images', state_slug,district_slug, chapter_slug, new_filename)


class CulturalChapter(models.Model):
    """
    Represents a specific chapter (like Food, Artforms) for a District.
    This is the parent object for all content on the page.
    """
    CHAPTER_CHOICES = [
        ('Architecture', 'Architecture'),
        ('Artforms', 'Artforms'),
        ('Cultural Sites', 'Cultural Sites'),
        ('Festivals & Fairs', 'Festivals & Fairs'),
        ('Food', 'Food'),
        ('Language', 'Language'),
        ('Local Politics', 'Local Politics'),
        ('Markets', 'Markets'),
        ('Political History', 'Political History'),
        ('Sports & Games', 'Sports & Games'),
        ('Stories', 'Stories'),
    ]

    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='cultural_chapters',null=True, blank=True)
    name = models.CharField(max_length=50, choices=CHAPTER_CHOICES)
    slug = models.SlugField(max_length=200, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated",blank=True, null=True)
    

    def get_absolute_url(self):
        return reverse('culture:cultural_chapter_detail', kwargs={
            'state_slug': self.district.state.slug,
            'district_slug': self.district.slug,
            'chapter_slug': self.slug
        })
    class Meta:
        
        unique_together = ('district', 'name')
        verbose_name = "Cultural Chapter"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.district.name}"

    def delete(self, *args, **kwargs):
        # Manually delete all content blocks first to handle polymorphic deletion
        for block in self.content_blocks.all():
            block.delete()
        super().delete(*args, **kwargs)

# Polymorphic Content Blocks for the Cultural Chapter

class ContentBlock(PolymorphicModel):
    """
    The generic, orderable base model for all content elements.
    It links to a CulturalChapter and knows its order on the page.
    """
    chapter = models.ForeignKey(CulturalChapter, on_delete=models.CASCADE, related_name='content_blocks')
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        #Fatching Block in the correct order.
        ordering = ['order']

    def __str__(self):
        return f"Block #{self.order} on {self.chapter}"

# ---- Specific, concrete block types 
# Each one inherits from ContentBlock and adds its own specific fields.

class HeadingBlockOne(ContentBlock):
    text = models.CharField(max_length=255)
    class Meta:
        verbose_name = "Heading 1"
    def __str__(self): return f"Heading 1: {self.text}"

class HeadingBlockTwo(ContentBlock):
    text = models.CharField(max_length=255)
    class Meta:
        verbose_name = "Heading 2"
    def __str__(self): return f"Heading 2: {self.text}"


class HeadingBlockThree(ContentBlock):
    text = models.CharField(max_length=255)
    class Meta:
        verbose_name = "Heading 3"
    
    def __str__(self):
        return f"Heading 3: {self.text}"

class ParagraphBlock(ContentBlock):
    # this Html Field  fom tinymce allows for rich text editing
    content = HTMLField(help_text="Formatted text, lists, and tables go here.")
    class Meta:
        verbose_name = "Paragraph Block"
    def __str__(self): return f"Paragraph: {self.content[:40]}..."






class ImageBlock(ContentBlock):
    image = models.ImageField(upload_to=get_seo_image_path,
                            validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
                            verbose_name="Original Image"
                    )
    caption = models.CharField(max_length=4000, blank=True)
    alt_text = models.CharField(max_length=4000, help_text="Accessibility text for screen readers.")
    
    # Add WebP versions with new names
    webp_large = ImageSpecField(
        source='image',  # Point to the existing image field
        processors=[ResizeToFit(1200, 1200)],
        format='WEBP',
        options={'quality': 80}
    )

    webp_medium = ImageSpecField(
        source='image',
        processors=[ResizeToFit(800, 800)],
        format='WEBP',
        options={'quality': 75}
    )

    webp_small = ImageSpecField(
        source='image',
        processors=[ResizeToFit(400, 400)],
        format='WEBP',
        options={'quality': 70}
    )





    class Meta:
        verbose_name = "Image Block"
    def __str__(self): 
        return f"Image: {self.caption or self.alt_text}"






class ReferenceBlock(ContentBlock):
    text = models.TextField()
    link = models.URLField(max_length=2000, blank=True, null=True) # <- After
    
    class Meta:
        verbose_name = "Reference Block"

    def __str__(self): 
        return f"Reference: {self.text[:75]}..."



