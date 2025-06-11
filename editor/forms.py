# editor/forms.py
from django import forms
from home.models import District
from culture.models import CulturalChapter

class ChapterSelectForm(forms.Form):
    # This form will help the user select or create a chapter.
    district = forms.ModelChoiceField(
        queryset=District.objects.all().order_by('state__name', 'name'),
        widget=forms.Select(attrs={'class': 'form-select block w-full mt-1 border-gray-300 rounded-md shadow-sm'})
    )
    chapter_name = forms.ChoiceField(
        choices=CulturalChapter.CHAPTER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select block w-full mt-1 border-gray-300 rounded-md shadow-sm'})
    )