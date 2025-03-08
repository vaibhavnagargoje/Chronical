from django.db import models
from django.utils.text import slugify
from home.models import District

class StatisticalChapter(models.Model):
    """
    A statistical chapter (e.g. Demography, Economy, etc.) for a given district.
    """
    CHAPTER_CHOICES = [
        ('Demography', 'Demography'),
        ('Agriculture', 'Agriculture'),
        ('Livestock & Fisheries', 'Livestock & Fisheries'),
        ('Education', 'Education'),
        ('Health', 'Health'),
        ('Environment', 'Environment'),
        ('Industry', 'Industry'),
        ('Labour', 'Labour'),
        ('Police & Judiciary', 'Police & Judiciary'),
        ('Transport & Communication', 'Transport & Communication'),
        ('Revenue & Expenditure', 'Revenue & Expenditure'),
        ('Schemes', 'Schemes'),
    ]

    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='statistical_chapters')
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


class StatisticalSection(models.Model):
    """
    A flexible model for repeated content blocks in a StatisticalChapter.
    """
    SECTION_TYPE_CHOICES = [
        ('heading', 'Heading'),
        ('subheading', 'Subheading'),
        ('text', 'Text'),
        ('image', 'Image'),
    ]
    chapter = models.ForeignKey(StatisticalChapter, on_delete=models.CASCADE, related_name='sections')
    section_type = models.CharField(max_length=20, choices=SECTION_TYPE_CHOICES)
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='statistical_images/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.chapter.name} - {self.section_type} - {self.order}"
