from django import forms
from home.models import District
from culture.models import CulturalChapter
from statistic.models import StatisticalChapter

class DataImportForm(forms.Form):
    # Add 'statistic' option to app_choice
    app_choice = forms.ChoiceField(
        choices=[('culture', 'Cultural'), ('statistic', 'Statistical')],
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
    
    image_zip = forms.FileField(
        label="Upload Image ZIP File (Optional)",
        required=False,
        widget=forms.ClearableFileInput(attrs={'accept': '.zip'}),
        help_text="Upload the zip file containing images that came with the HTML download."
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically set chapter choices based on app_choice
        if args and 'app_choice' in args[0]:
            app_choice = args[0]['app_choice']
            if app_choice == 'statistic':
                self.fields['chapter_name'].choices = StatisticalChapter.CHAPTER_CHOICES
            else:
                self.fields['chapter_name'].choices = CulturalChapter.CHAPTER_CHOICES