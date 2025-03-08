from django.shortcuts import render, get_object_or_404
from home.models import State
from .models import StatisticalChapter

def statistical_chapter_detail(request, state_slug, district_slug, chapter_slug):
    """
    Show a particular statistical chapter and all its sections.
    """
    state = get_object_or_404(State, slug=state_slug)
    district = get_object_or_404(state.districts, slug=district_slug)
    chapter = get_object_or_404(district.statistical_chapters, slug=chapter_slug)
    sections = chapter.sections.all()
    
    context = {
        'state': state,
        'district': district,
        'chapter': chapter,
        'sections': sections,
    }
    return render(request, 'statistics/chapter_detail.html', context)
