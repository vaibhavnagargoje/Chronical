# # editor/forms.py
# from django import forms
# from home.models import District
# from culture.models import CulturalChapter
# from statistic.models import StatisticalChapter # To get choices

# class ChapterSelectForm(forms.Form):
#     # This form will help the user select or create a chapter.
#     district = forms.ModelChoiceField(
#         queryset=District.objects.all().order_by('state__name', 'name'),
#         widget=forms.Select(attrs={'class': 'form-select block w-full mt-1 border-gray-300 rounded-md shadow-sm'})
#     )
#     chapter_name = forms.ChoiceField(
#         choices=CulturalChapter.CHAPTER_CHOICES,
#         widget=forms.Select(attrs={'class': 'form-select block w-full mt-1 border-gray-300 rounded-md shadow-sm'})
#     )






# editor/forms.py
from django import forms
from home.models import District
from culture.models import CulturalChapter
from statistic.models import StatisticalChapter

class ChapterSelectForm(forms.Form):
    # This form helps the user select or create a chapter.
    district = forms.ModelChoiceField(
        queryset=District.objects.all().order_by('state__name', 'name'),
        widget=forms.Select(attrs={'class': 'form-select block w-full mt-1 border-gray-300 rounded-md shadow-sm'})
    )
    # The 'choices' will be set dynamically below
    chapter_name = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-select block w-full mt-1 border-gray-300 rounded-md shadow-sm'})
    )

    def __init__(self, *args, **kwargs):
        """
        This special method dynamically sets the chapter_name choices
        based on which app we are editing ('culture' or 'statistic').
        """
        # Get the 'app_label' we will pass in from the view, defaulting to 'culture'
        app_label = kwargs.pop('app_label', 'culture')

        # Run the standard form initialization
        super().__init__(*args, **kwargs)

        # Now, set the correct choices based on the app
        if app_label == 'statistic':
            self.fields['chapter_name'].choices = StatisticalChapter.CHAPTER_CHOICES
        else: # Default to culture
            self.fields['chapter_name'].choices = CulturalChapter.CHAPTER_CHOICES