from django.db import models
from django.utils.text import slugify
from home.models import District

# -----------------------------------------------
# Core Models
# -----------------------------------------------
class CulturalChapter(models.Model):
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
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='cultural_chapters', blank=True, null=True)
    cityname = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=50, choices=CHAPTER_CHOICES, blank=True, null=True)
    slug = models.SlugField(max_length=200, blank=True, unique=False)

    class Meta:
        unique_together = ('district','name')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.district.name if self.district else 'No District'}"


class CulturalSection(models.Model):
    chapter = models.ForeignKey(CulturalChapter, on_delete=models.CASCADE, related_name='sections', blank=True, null=True)
    order = models.PositiveIntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.chapter.name if self.chapter else 'No Chapter'} - Section {self.order}"


class Heading(models.Model):
    section = models.ForeignKey(CulturalSection, on_delete=models.CASCADE, related_name='headings', blank=True, null=True)
    text = models.CharField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Heading: {self.text}"


class Subheading(models.Model):
    section = models.ForeignKey(CulturalSection, on_delete=models.CASCADE, related_name='subheadings', blank=True, null=True)
    text = models.CharField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Subheading: {self.text}"


class Text(models.Model):
    section = models.ForeignKey(CulturalSection, on_delete=models.CASCADE, related_name='texts', blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Text: {self.content[:50] if self.content else 'No Content'}..."





class Image(models.Model):
    """
    An image within a CulturalSection.
    """
    section = models.ForeignKey(CulturalSection, on_delete=models.CASCADE, related_name='images', blank=True, null=True)
    image = models.ImageField(upload_to='culture_images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    order = models.PositiveIntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image"




class Reference(models.Model):
    section = models.ForeignKey(CulturalSection, on_delete=models.CASCADE, related_name='references', blank=True, null=True)
    text = models.CharField(max_length=255, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Reference: {self.text if self.text else 'No Text'}"