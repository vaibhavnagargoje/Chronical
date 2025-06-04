from django.db import models

# Create your models here.
from django.db import models
from django.utils.text import slugify

class State(models.Model):
    """
    Represents an Indian State (e.g. Maharashtra, Gujarat, etc.)
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


from django.core.validators import FileExtensionValidator



class District(models.Model):
    """
    Represents a District belonging to a specific State.
    """
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='districts')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    introduction = models.TextField(blank=True, null=True)  # Brief introduction text
    
    # Ensure uniqueness of (state, name)
    class Meta:
        unique_together = ('state', 'name')
        

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}, {self.state.name}"

class DistrictParagraph(models.Model):
    """
    Additional paragraphs for district introduction
    """
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='paragraphs')
    content = models.TextField()
    
    
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
    content = models.TextField()
    
    
    
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