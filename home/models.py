from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from tinymce.models import HTMLField
from django.db import models
from django.urls import reverse




class State(models.Model):
    """
    Represents an Indian State (e.g. Maharashtra, Gujarat, etc.)
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    state_code = models.CharField(max_length=5, unique=True, null=True, blank=True)    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class District(models.Model):
    """Represents a District belonging to a specific State.
    """
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='districts')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    introduction = HTMLField(blank=True, null=True, verbose_name="Introduction")  # Properly configure HTMLField with default configuration

    
    # Ensure uniqueness of (state, name)
    class Meta:
        unique_together = ('state', 'name')
        

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}, {self.state.name}"
    
    def get_absolute_url(self):
        return reverse('home:district_detail', kwargs={
            'state_slug': self.state.slug,
            'district_slug': self.slug
        })

class DistrictSVG(models.Model):
    """
    SVG representation of a district
    """
    district = models.OneToOneField(District, on_delete=models.CASCADE, related_name='districtsvg')
    svg_content = models.TextField(verbose_name="SVG Content")  # Store SVG content as text
    district_code = models.CharField(max_length=10, unique=True, null=True, blank=True) 
    
    def get_absolute_url(self):
        # This allows us to use `district.get_absolute_url` in templates
        return reverse('home:district_detail', kwargs={
            'state_slug': self.state.slug,
            'district_slug': self.slug
        })
    def __str__(self):
        return f"SVG for {self.district.name}"


class DistrictParagraph(models.Model):
    """
    Additional paragraphs for district introduction
    """
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='paragraphs')
    content = HTMLField(blank=True, null=True, verbose_name="Content")  # Update HTMLField with proper configuration
    
    
    def __str__(self):
        return f"Paragraph for {self.district.name}"

class DistrictImage(models.Model):
    """
    Images related to a district
    """
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        upload_to='district_images/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])]
    )
    caption = models.CharField(max_length=255, blank=True)
    alt_text = models.CharField(max_length=255, blank=True)
    
    
    def __str__(self):
        return f"Image for {self.district.name} "


      

class DistrictQuickFact(models.Model):
    """
    Quick facts about a district (key-value pairs with icons)
    """
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='quick_facts')
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=255, blank=True, null=True)
    

    
    def __str__(self):
        return f"{self.title} - {self.district.name}"

class DistrictSection(models.Model):
    """
    Sections like Geography, Heritage, etc.
    """
    SECTION_TYPES = [
        ('geography', 'Geography'),
        ('heritage', 'Heritage'),
        ('culture', 'Culture'),
        ('economy', 'Economy'),
        ('tourism', 'Tourism'),
        ('other', 'Other'),
    ]
    
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='sections')
    section_type = models.CharField(max_length=20, choices=SECTION_TYPES)
    title = models.CharField(max_length=100)
    
    class Meta:
        
        unique_together = ('district', 'section_type')
    
    def __str__(self):
        return f"{self.title} - {self.district.name}"

class SectionParagraph(models.Model):
    """
    Paragraphs within a section
    """
    section = models.ForeignKey(DistrictSection, on_delete=models.CASCADE, related_name='paragraphs')
    content = HTMLField(blank=True, null=True, verbose_name="Content")  # Update HTMLField with proper configuration
    
    
    
    def __str__(self):
        return f"Paragraph for {self.section.title}"

class SectionImage(models.Model):
    """
    Images related to a section
    """
    section = models.ForeignKey(DistrictSection, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        upload_to='section_images/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])]
    )
    caption = models.CharField(max_length=255, blank=True)
    alt_text = models.CharField(max_length=255, blank=True)
    
    
    
    def __str__(self):
        return f"Image for {self.section.title} "