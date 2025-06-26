from django import forms
from home.models import District
from culture.models import CulturalChapter

class DataImportForm(forms.Form):
    # No changes to the existing fields
    app_choice = forms.ChoiceField(
        choices=[('culture', 'Cultural')],
        label="Select App Type"
    )
    district = forms.ModelChoiceField(
        queryset=District.objects.all().order_by('state__name', 'name'),
        label="Select District"
    )
    chapter_name = forms.ChoiceField(
        choices=CulturalChapter.CHAPTER_CHOICES,
        label="Select Chapter"
    )
    html_file = forms.FileField(
        label="Upload HTML File",
        widget=forms.ClearableFileInput(attrs={'accept': '.html'}),
        help_text="Upload the .html file from the Google Doc."
    )
    
    # --- ADD THIS NEW FIELD ---
    image_zip = forms.FileField(
        label="Upload Image ZIP File (Optional)",
        required=False, # Make it optional
        widget=forms.ClearableFileInput(attrs={'accept': '.zip'}),
        help_text="Upload the zip file containing images that came with the HTML download."
    )