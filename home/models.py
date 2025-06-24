from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from tinymce.models import HTMLField
from django.db import models
from django.urls import reverse

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
import subprocess
import os
from django.conf import settings




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
    original_image  = models.ImageField(
        upload_to='district_images/originals/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
        verbose_name="Original Image",
        blank=True, null=True,
    )
    caption = models.CharField(max_length=255, blank=True)
    alt_text = models.CharField(max_length=255, blank=True)
    
    webp_large = ImageSpecField(source='original_image',
                                processors=[ResizeToFit(1200, 1200)],
                                format='WEBP',
                                options={'quality': 80},)

    webp_medium = ImageSpecField(source='original_image',
                                 processors=[ResizeToFit(800, 800)],
                                    format='WEBP',
                                    options={'quality': 75},)
    webp_small = ImageSpecField(source='original_image',
                                    processors=[ResizeToFit(400, 400)],
                                        format='WEBP',
                                        options={'quality': 70},)
    
    def get_upload_path(instance, filename):
        """ generate SEO-friendly upload path for images """
        ext = filename.split('.')[-1]
        base_name = slugify(f"{instance.district.state.name}-{instance.district.name}")
        if instance.caption:
            base_name += f"-{slugify(instance.caption[:30])}"
        return f'district_images/originals/{base_name}.{ext}'
    
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


class GIFImage(models.Model):     #SectionImage 
    """
    Images related to a section
    """
    district  = models.ForeignKey(District, on_delete=models.CASCADE, related_name='gif_images')
    original_file = models.FileField(
        upload_to='gif_images/originals/', # Store originals
        validators=[FileExtensionValidator(['gif'])],
        verbose_name="Original GIF",
        blank=True, null=True,
    )
    optimized_video = models.FileField(upload_to='gif_images/videos/',blank=True, null=True,editable=False)
    caption = models.CharField(max_length=255, blank=True)
    alt_text = models.CharField(max_length=255, blank=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.original_file and not self.optimized_video:
            try:
                input_path = self.original_file.path
                # Verify input file exists
                if not os.path.exists(input_path):
                    print(f"Input file not found: {input_path}")
                    return
                    
                # Create output directory
                output_dir = os.path.join(settings.MEDIA_ROOT, 'gif_images', 'videos')
                os.makedirs(output_dir, exist_ok=True)
                
                # Prepare output path
                output_filename = f"{os.path.splitext(os.path.basename(input_path))[0]}.mp4"
                output_path = os.path.join(output_dir, output_filename)
                
                command = [
                    settings.FFMPEG_PATH,
                    '-i', input_path,
                    '-movflags', '+faststart',
                    '-pix_fmt', 'yuv420p',
                    '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2',
                    '-y', output_path
                ]
                
                # Print command for debugging
                print("Executing:", " ".join(command))
                
                result = subprocess.run(
                    command,
                    check=True,
                    capture_output=True,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW  # For Windows
                )
                
                # Update model field
                self.optimized_video.name = os.path.join('gif_images', 'videos', output_filename)
                super().save(update_fields=['optimized_video'])
                
            except subprocess.CalledProcessError as e:
                print(f"❌ FFmpeg Error (code {e.returncode}):")
                print(e.stderr)
            except FileNotFoundError:
                print(f"🔥 FFmpeg executable not found at: {settings.FFMPEG_PATH}")
            except Exception as e:
                print(f"🚨 Unexpected error: {str(e)}")

    def __str__(self):
        return f"Animation for {self.district.name}"
    