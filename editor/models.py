from django.db import models
from django.contrib.auth.models import User
from culture.models import CulturalChapter
from statistic.models import StatisticalChapter

class SuggestEdit(models.Model):
    EDIT_TYPE_CHOICES = [
        ('correction', 'Correction of factual error'),
        ('addition', 'Addition of new information'),
        ('clarification', 'Clarification of existing content'),
        ('update', 'Update outdated information'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('in_review', 'In Review'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=255)
    email = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Chapter Information
    app_label = models.CharField(max_length=50)  # 'culture' or 'statistic'
    chapter_id = models.PositiveIntegerField()
    section = models.CharField(max_length=255, blank=True)
    
    # Edit Details
    edit_type = models.CharField(max_length=20, choices=EDIT_TYPE_CHOICES)
    current_text = models.TextField(blank=True)
    suggested_text = models.TextField()
    reason = models.TextField()
    sources = models.TextField(blank=True)
    
    # File Upload
    supporting_file = models.FileField(upload_to='suggest_edits/', blank=True, null=True)
    
    # Notifications
    notify_on_review = models.BooleanField(default=False)
    
    # Status and Timestamps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_suggestions')
    review_notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Suggest Edit'
        verbose_name_plural = 'Suggest Edits'
    
    def __str__(self):
        return f"Edit suggestion by {self.name} - {self.edit_type}"
    
    def get_chapter(self):
        """Get the actual chapter object based on app_label and chapter_id"""
        if self.app_label == 'culture':
            try:
                return CulturalChapter.objects.get(id=self.chapter_id)
            except CulturalChapter.DoesNotExist:
                return None
        elif self.app_label == 'statistic':
            try:
                return StatisticalChapter.objects.get(id=self.chapter_id)
            except StatisticalChapter.DoesNotExist:
                return None
        return None
    
    def get_chapter_title(self):
        """Get the chapter title for display"""
        chapter = self.get_chapter()
        return f"{chapter.name} - {chapter.district.name}" if chapter else "Unknown Chapter"



class IntroductionEdit(models.Model):
    """
    Model for suggesting edits to District introductions
    """
    EDIT_TYPE_CHOICES = [
        ('correction', 'Correction of factual error'),
        ('addition', 'Addition of new information'),
        ('clarification', 'Clarification of existing content'),
        ('update', 'Update outdated information'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('in_review', 'In Review'),
    ]
    
    SECTION_CHOICES = [
        ('introduction', 'Introduction Text'),
        ('quick_facts', 'Quick Facts'),
        ('images', 'Images'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=255)
    email = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # District Information
    district = models.ForeignKey('home.District', on_delete=models.CASCADE, related_name='intro_suggestions')
    section = models.CharField(max_length=50, choices=SECTION_CHOICES, default='introduction')
    
    # Edit Details
    edit_type = models.CharField(max_length=20, choices=EDIT_TYPE_CHOICES)
    current_text = models.TextField(blank=True, help_text="Current text that needs to be edited")
    suggested_text = models.TextField(help_text="Your suggested text or correction")
    reason = models.TextField(help_text="Explanation for this edit")
    sources = models.TextField(blank=True, help_text="References or sources to support your edit")
    
    # File Upload
    supporting_file = models.FileField(upload_to='suggest_edits/intro/', blank=True, null=True)
    
    # Notifications
    notify_on_review = models.BooleanField(default=False)
    
    # Status and Timestamps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_intro_suggestions')
    review_notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Introduction Edit Suggestion'
        verbose_name_plural = 'Introduction Edit Suggestions'
    
    def __str__(self):
        return f"Intro edit suggestion by {self.name} - {self.district.name} ({self.edit_type})"
    
    def get_district_name(self):
        """Get the district name for display"""
        return f"{self.district.name}, {self.district.state.name}"