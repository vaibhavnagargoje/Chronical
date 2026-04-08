from django.db import models
from django.utils.text import slugify
from home.models import District
from django.urls import reverse
from polymorphic.models import PolymorphicModel
from tinymce.models import HTMLField
import os 
import uuid


from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from django.core.validators import FileExtensionValidator

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

    state_slug = instance.chapter.district.state.slug if instance.chapter.district.state else 'unknown-state'
    district_slug = instance.chapter.district.slug if instance.chapter.district else 'unknown-district'
    chapter_slug = instance.chapter.slug

    return os.path.join('statistic', 'images', state_slug, district_slug, chapter_slug, new_filename)



class StatisticalChapter(models.Model):
    
    CHAPTER_CHOICES = [
        ('Agriculture', 'Agriculture'),
        ('Demography', 'Demography'),
        ('Education', 'Education'),
        ('Elections', 'Elections'),
        ('Environment', 'Environment'),
        ('Health', 'Health'),
        ('Industry', 'Industry'),
        ('Labor', 'Labor'),
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


    def delete(self, *args, **kwargs):
        # Manually delete all content blocks first to handle polymorphic deletion
        for block in self.content_blocks.all():
            block.delete()
        super().delete(*args, **kwargs)

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
    image = models.ImageField(upload_to=get_seo_image_path,verbose_name="Original Image")
    caption = models.CharField(max_length=4000, blank=True)
    alt_text = models.CharField(max_length=4000, help_text="Accessibility text for screen readers.")
    img_ref = models.CharField(max_length=4000, blank=True, null=True, help_text="Reference for the image source")

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
    def __str__(self): return f"Image: {self.caption or self.alt_text}"


class ReferenceBlock(StatisticContentBlock):
    text = models.TextField()
    link = models.URLField(max_length=2000, blank=True, null=True)
    class Meta:
        verbose_name = "Reference Block"
    def __str__(self): 
        return f"Reference: {self.text[:75]}..."


def get_statistic_chart_path(instance, filename):
    """
    Generates a unique path for uploaded chart HTML files.
    Example: statistic/charts/population-growth-a1b2c3d4.html
    """
    base_name = slugify(instance.title or uuid.uuid4().hex)
    ext = os.path.splitext(filename)[1] or '.html'  # Ensure it has a .html extension
    unique_id = uuid.uuid4().hex[8]
    new_filename = f"{base_name}-{unique_id}{ext}"

    
    state_slug = instance.chapter.district.state.slug if instance.chapter.district.state else 'unknown-state'
    district_slug = instance.chapter.district.slug if instance.chapter.district else 'unknown-district'
    chapter_slug = instance.chapter.slug
    return os.path.join('statistic', 'charts', state_slug, district_slug, chapter_slug, new_filename)

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
        return f'Chart Block: {self.title or "  Untitled"}'


class DynamicChartBlock(StatisticContentBlock):
    """
    A block for displaying dynamic, database-driven charts.
    References a ChartTemplate from the charthandler app instead of a static HTML file.
    Works alongside the existing ChartBlock for backward compatibility.
    """
    chart_template = models.ForeignKey(
        'charthandler.ChartTemplate',
        on_delete=models.PROTECT,
        related_name='dynamic_blocks',
        help_text="Select the chart template to render"
    )
    title_override = models.CharField(
        max_length=255,
        blank=True,
        default='',
        help_text="Optional: Override the chart template's default title"
    )

    class Meta:
        verbose_name = "Dynamic Chart Block"

    def __str__(self):
        title = self.title_override or (self.chart_template.title if self.chart_template_id else 'No Template')
        return f'Dynamic Chart: {title}'

    def get_chart_title(self):
        return self.title_override or self.chart_template.title

















