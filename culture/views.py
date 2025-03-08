from django.shortcuts import render, get_object_or_404
from home.models import State
from .models import CulturalChapter

def cultural_chapter_detail(request, state_slug, district_slug, chapter_slug):
    """
    Show a particular cultural chapter and all its sections.
    """
    # First, get the correct state
    state = get_object_or_404(State, slug=state_slug)
    # Then get the district within that state
    district = get_object_or_404(state.districts, slug=district_slug)
    # Finally, get the cultural chapter within that district
    chapter = get_object_or_404(district.cultural_chapters, slug=chapter_slug)
    
    # Get all sections in the correct order
    sections = chapter.sections.all()

    context = {
        'state': state,
        'district': district,
        'chapter': chapter,
        'sections': sections,
    }
    return render(request, 'culture/chapter_detail.html', context)
