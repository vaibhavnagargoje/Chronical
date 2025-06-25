from django.db import models
from django.core.exceptions import ValidationError

from home.models import District
from culture.models import CulturalChapter
from statistic.models import StatisticalChapter

# Create your models here.


class CulturalSidePanal(models.Model):
    """
    A word/definition pair scoped to a specific chapter.
    The district is stored for efficient filtering and API lookups.
    """
    cultural_chapter = models.ForeignKey(CulturalChapter, on_delete=models.CASCADE, help_text="Choose a Cultural Chapter if this entry is related to one", related_name="cultural_chapters", verbose_name='Cultural Chapter', null=True, blank=True)
   
    word = models.CharField(max_length=200, verbose_name='Word') 
    definition = models.TextField(verbose_name='Definition')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        ordering = ['word']
        verbose_name_plural = 'Cultural Side Panals all records'
       

    def __str__(self):
        return self.word

class StatisticalSidePanal(models.Model):
    """
    A word/definition pair scoped to a specific chapter.
    The district is stored for efficient filtering and API lookups.
    """
    statistical_chapter = models.ForeignKey(StatisticalChapter, on_delete=models.CASCADE, help_text="Choose a Statistical Chapter if this entry is related to one", related_name="statistical_chapters", verbose_name='Statistical Chapter', null=True, blank=True)

    word = models.CharField(max_length=200, verbose_name='Statistical Word')
    definition = models.TextField(verbose_name='Statistical Definition')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    

    class Meta:
        
        ordering = ['word']
        verbose_name_plural = 'Stat Side Panals all records'
       

    def __str__(self):
        return self.word
   



class StatisticalSidePanelManager(StatisticalChapter):
    """
    This is a Proxy Model. It uses the same database table as the original
    StatisticalChapter but gives us a new, separate place in the admin
    to manage the side panels associated with each chapter.
    """
    class Meta:
        proxy = True
        verbose_name = 'Statistical Side Panel Manager'
        verbose_name_plural = 'Statistical Side Panel Managers'


class CulturalSidePanelManager(CulturalChapter):
    """
    This is a Proxy Model. It uses the same database table as the original
    CulturalChapter but gives us a new, separate place in the admin
    to manage the side panels associated with each chapter.
    """
    class Meta:
        proxy = True
        verbose_name = 'Cultural Side Panel Manager'
        verbose_name_plural = 'Cultural Side panel Managers'