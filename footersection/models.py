from django.db import models
from tinymce.models import HTMLField


# Create your models here.
class Project(models.Model):
    text = HTMLField(help_text="Enter the project text here.",blank=True, null=True)

class Partnership(models.Model):
    text = HTMLField(help_text="Enter the partnership text here.",blank=True, null=True)

class Careers(models.Model):
    text = HTMLField(help_text="Enter the careers text here.",blank=True, null=True)

class Careers_post(models.Model):
    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
    ]
    
    EXPERIENCE_LEVEL_CHOICES = [
        ('entry', 'Entry Level'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior Level'),
        ('executive', 'Executive'),
    ]
    
    title = models.CharField(max_length=200, help_text="Job title")
    department = models.CharField(max_length=100, help_text="Department/Team")
    location = models.CharField(max_length=100, help_text="Job location")
    employment_type = models.CharField(
        max_length=20, 
        choices=EMPLOYMENT_TYPE_CHOICES, 
        default='full_time',
        help_text="Type of employment"
    )
    experience_level = models.CharField(
        max_length=20, 
        choices=EXPERIENCE_LEVEL_CHOICES, 
        default='entry',
        help_text="Required experience level"
    )
    salary_range = models.CharField(max_length=100, blank=True, null=True, help_text="Salary range (optional)")
    description = HTMLField(help_text="Job description and responsibilities")
    requirements = HTMLField(help_text="Job requirements and qualifications")
    benefits = HTMLField(blank=True, null=True, help_text="Benefits and perks (optional)")
    application_deadline = models.DateField(blank=True, null=True, help_text="Application deadline (optional)")
    is_active = models.BooleanField(default=True, help_text="Is this job posting active?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Career Post"
        verbose_name_plural = "Career Posts"
    
    def __str__(self):
        return f"{self.title} - {self.department}"

class Terms(models.Model):
    text = HTMLField(help_text="Enter the terms and conditions text here.",blank=True, null=True)

class Disclaimer(models.Model):
    text = HTMLField(help_text="Enter the disclaimer text here.",blank=True, null=True)


class Message(models.Model):
    name = models.CharField(max_length=100, help_text="Full name of the person")
    email = models.EmailField(help_text="Email address")
    subject = models.CharField(max_length=200, help_text="Message subject")
    message = models.TextField(help_text="Message content")
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, help_text="Has this message been read?")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Message"
        verbose_name_plural = "Messages"
    
    def __str__(self):
        return f"{self.name} - {self.subject[:50]}"