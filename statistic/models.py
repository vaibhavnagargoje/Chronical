from django.db import models
from django.utils.text import slugify
from home.models import District
from django.urls import reverse
from polymorphic.models import PolymorphicModel
from tinymce.models import HTMLField
import os 
import uuid


def get_seo_image_path(instance, filename):
    """
    Generates a unique, SEO-friendly path for an uploaded image.
    Example: statistic/images/health-statistics-a1b2c3d4.jpg
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

    return os.path.join('statistic', 'images', new_filename)



class StatisticalChapter(models.Model):
    
    CHAPTER_CHOICES = [
        ('Agriculture', 'Agriculture'),
        ('Demography', 'Demography'),
        ('Education', 'Education'),
        ('Environment', 'Environment'),
        ('Health', 'Health'),
        ('Industry', 'Industry'),
        ('Labour', 'Labour'),
        ('Livestock & Fisheries', 'Livestock & Fisheries'),
        ('Police & Judiciary', 'Police & Judiciary'),
        ('Revenue & Expenditure', 'Revenue & Expenditure'),
        ('Transport & Communication', 'Transport & Communication'),
    ]

    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='statistical_chapters')
    name = models.CharField(max_length=200, choices=CHAPTER_CHOICES)  # Dropdown selection
    slug = models.SlugField(max_length=200, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Last Updated', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('statistic:statistical_chapter_detail', kwargs={
            'state_slug': self.district.state.slug,
            'district_slug':self.district.slug,
            'chapter_slug':self.slug
        })
    

    class Meta:
        unique_together = ('district', 'name')
        verbose_name = 'Statistical Chapter'
        ordering = ['name']


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.district.name}"


class StatisticContentBlock(PolymorphicModel):
    chapter= models.ForeignKey(StatisticalChapter, on_delete=models.CASCADE, related_name="content_blocks")
    order= models.PositiveIntegerField(default=0, verbose_name='Order')

    class Meta:
        ordering =['order']
    
    def __str__(self):
        return f"Block #{self.order} in {self.chapter.name}"

    
# Polymorphic Content Blocks for the Statistical Chapter for different types of content

class HeadingBlockOne(StatisticContentBlock):
    text = models.CharField(max_length=255, verbose_name='Heading 1')
    
    class Meta:
        verbose_name ="Heading 1"
    
    def __str__(self):
        return f"Heading 1:{self.text}"
    
class HeadingBlockTwo(StatisticContentBlock):
    text = models.CharField(max_length=255, verbose_name='Heading 2')
    
    class Meta:
        verbose_name ="Heading 2"
    
    def __str__(self):
        return f"Heading 2:{self.text}"
    
class HeadingBlockThree(StatisticContentBlock):
    text = models.CharField(max_length=255, verbose_name='Heading 3')
    
    class Meta:
        verbose_name ="Heading 3"
    
    def __str__(self):
        return f"Heading 3:{self.text}"



class ParagraphBlock(StatisticContentBlock):
    content = HTMLField(verbose_name='formatted text for context')
    class Meta:
        verbose_name = "Paragraph Block"
    
    def __str__(self):
        return f"Paragraph Block: {self.content[:40]}..."
    
class ImageBlock(StatisticContentBlock):
    image = models.ImageField(upload_to=get_seo_image_path)
    caption = models.CharField(max_length=4000, blank=True)
    alt_text = models.CharField(max_length=4000, help_text="Accessibility text for screen readers.")
    class Meta:
        verbose_name = "Image Block"
    def __str__(self): return f"Image: {self.caption or self.alt_text}"


class ReferenceBlock(StatisticContentBlock):
    text = models.CharField(max_length=255)
    link = models.URLField(blank=True, null=True)
    class Meta:
        verbose_name = "Reference Block"
    def __str__(self): return f"Reference: {self.text}"


def get_statistic_chart_path(instance, filename):
    """
    Generates a unique path for uploaded chart HTML files.
    Example: statistic/charts/population-growth-a1b2c3d4.html
    """
    base_name = slugify(instance.title or uuid.uuid4().hex)
    ext = os.path.splitext(filename)[1] or '.html'  # Ensure it has a .html extension
    unique_id = uuid.uuid4().hex[8]
    new_filename = f"{base_name}-{unique_id}{ext}"
    return os.path.join('statistic', 'charts', new_filename)

class ChartBlock(StatisticContentBlock):
    """
    A block for displaying charts or graphs.
    """
    title = models.CharField(max_length=255, help_text="Title of the chart e.g., 'Population Growth'", blank=True, null=True)
    chart_html_file = models.FileField(
        upload_to=get_statistic_chart_path,
        help_text= "Upload on The PreGenrated  .html File for the Chart"
 )
    
    def get_chart_url(self):
        """
        Returns the URL for the dedicated serving view, not the raw media URL.
        """
        return reverse('statistic:serve_chart_html', args=[self.id])
    class Meta:
        verbose_name = "Chart Block (HTML Upload)"
    def __str__(self):
        return f'Chart Block: {self.title or "Untitled"}'



















# old models for statistical section
# class StatisticalSection(models.Model):
#     """
#     A flexible model for repeated content blocks in a StatisticalChapter.
#     """
#     SECTION_TYPE_CHOICES = [
#         ('heading', 'Heading'),
#         ('subheading', 'Subheading'),
#         ('text', 'Text'),
#         ('image', 'Image'),
#     ]
#     chapter = models.ForeignKey(StatisticalChapter, on_delete=models.CASCADE, related_name='sections')
#     section_type = models.CharField(max_length=20, choices=SECTION_TYPE_CHOICES)
#     title = models.CharField(max_length=255, blank=True, null=True)
#     content = models.TextField(blank=True, null=True)
#     image = models.ImageField(upload_to='statistical_images/', blank=True, null=True)
#     order = models.PositiveIntegerField(default=0)

#     class Meta:
#         ordering = ['order']

#     def __str__(self):
#         return f"{self.chapter.name} - {self.section_type} - {self.order}"
