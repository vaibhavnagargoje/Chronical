from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from tinymce.models import HTMLField
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

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
    
    @property
    def has_valid_video(self):
        """Check if optimized video exists and is accessible"""
        if not self.optimized_video:
            return False
        try:
            return os.path.exists(self.optimized_video.path)
        except (ValueError, AttributeError):
            return False
    
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
                print("Will fallback to original GIF in template")
            except FileNotFoundError:
                print(f"🔥 FFmpeg executable not found at: {settings.FFMPEG_PATH}")
                print("Will fallback to original GIF in template")
            except Exception as e:
                print(f"🚨 Unexpected error: {str(e)}")
                print("Will fallback to original GIF in template")

    def __str__(self):
        return f"Animation for {self.district.name}"


class DeveloperCheck(models.Model):
    """
    Developer review status for Cultural and Statistical chapters
    """
    # Reference to existing chapters
    cultural_chapter = models.OneToOneField(
        'culture.CulturalChapter', 
        on_delete=models.CASCADE, 
        null=True, blank=True,
        related_name='developer_check'
    )
    statistical_chapter = models.OneToOneField(
        'statistic.StatisticalChapter', 
        on_delete=models.CASCADE, 
        null=True, blank=True,
        related_name='developer_check'
    )
    
    # Developer checkboxes
    ready_for_review = models.BooleanField(default=False, verbose_name="Ready for Review")
    reviewed = models.BooleanField(default=False, verbose_name="Developer Reviewed")
    
    # User tracking
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dev_created_reviews')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='dev_reviewed_chapters')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Developer Check"
        verbose_name_plural = "Developer Checks"
        ordering = ['-updated_at']
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.cultural_chapter and self.statistical_chapter:
            raise ValidationError("Cannot select both cultural and statistical chapter.")
        if not self.cultural_chapter and not self.statistical_chapter:
            raise ValidationError("Must select either a cultural or statistical chapter.")
    
    def save(self, *args, **kwargs):
        if self.reviewed and not self.reviewed_at:
            from django.utils import timezone
            self.reviewed_at = timezone.now()
        super().save(*args, **kwargs)
    
    @property
    def chapter_name(self):
        if self.cultural_chapter:
            return self.cultural_chapter.name
        elif self.statistical_chapter:
            return self.statistical_chapter.name
        return "No Chapter"
    
    @property
    def district(self):
        if self.cultural_chapter:
            return self.cultural_chapter.district
        elif self.statistical_chapter:
            return self.statistical_chapter.district
        return None
    
    def __str__(self):
        status = "✅ Dev Reviewed" if self.reviewed else ("📋 Dev Ready" if self.ready_for_review else "📝 Dev Draft")
        return f"{status} | {self.chapter_name} - {self.district.name if self.district else 'No District'}"



class FinalCheck(models.Model):
    """
    Final review status for Cultural and Statistical chapters
    """
    # Reference to existing chapters
    cultural_chapter = models.OneToOneField(
        'culture.CulturalChapter', 
        on_delete=models.CASCADE, 
        null=True, blank=True,
        related_name='final_check'
    )
    statistical_chapter = models.OneToOneField(
        'statistic.StatisticalChapter', 
        on_delete=models.CASCADE, 
        null=True, blank=True,
        related_name='final_check'
    )
    
    # Final checkboxes
    ready_for_review = models.BooleanField(default=False, verbose_name="Ready for Final Review")
    reviewed = models.BooleanField(default=False, verbose_name="Final Reviewed")
    
    # User tracking
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='final_created_reviews')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='final_reviewed_chapters')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Final Check"
        verbose_name_plural = "Final Checks"
        ordering = ['-updated_at']
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.cultural_chapter and self.statistical_chapter:
            raise ValidationError("Cannot select both cultural and statistical chapter.")
        if not self.cultural_chapter and not self.statistical_chapter:
            raise ValidationError("Must select either a cultural or statistical chapter.")
    
    def save(self, *args, **kwargs):
        if self.reviewed and not self.reviewed_at:
            from django.utils import timezone
            self.reviewed_at = timezone.now()
        super().save(*args, **kwargs)
    
    @property
    def chapter_name(self):
        if self.cultural_chapter:
            return self.cultural_chapter.name
        elif self.statistical_chapter:
            return self.statistical_chapter.name
        return "No Chapter"
    
    @property
    def district(self):
        if self.cultural_chapter:
            return self.cultural_chapter.district
        elif self.statistical_chapter:
            return self.statistical_chapter.district
        return None
    
    def __str__(self):
        status = "✅ Final Reviewed" if self.reviewed else ("📋 Final Ready" if self.ready_for_review else "📝 Final Draft")
        return f"{status} | {self.chapter_name} - {self.district.name if self.district else 'No District'}"
