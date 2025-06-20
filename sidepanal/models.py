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
       

    def __str__(self):
        return self.word
   
