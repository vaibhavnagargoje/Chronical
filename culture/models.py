from django.db import models
from django.utils.text import slugify
from home.models import District

class CulturalChapter(models.Model):
    """
    A cultural chapter (e.g. Food, Folk Dance, Festivals, etc.) for a given district.
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

    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='cultural_chapters')
    name = models.CharField(max_length=50, choices=CHAPTER_CHOICES)  # Dropdown selection
    slug = models.SlugField(max_length=200, blank=True, unique=True)

    class Meta:
        unique_together = ('district', 'name')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.district.name}"


class CulturalSection(models.Model):
    """
    A flexible model for repeated content blocks in a CulturalChapter.
    Each block can be a heading, subheading, text, or image.
    """
    SECTION_TYPE_CHOICES = [
        ('heading', 'Heading'),
        ('subheading', 'Subheading'),
        ('text', 'Text'),
        ('image', 'Image'),
    ]
    chapter = models.ForeignKey(CulturalChapter, on_delete=models.CASCADE, related_name='sections')
    section_type = models.CharField(max_length=20, choices=SECTION_TYPE_CHOICES)
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='culture_images/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.chapter.name} - {self.section_type} - {self.order}"