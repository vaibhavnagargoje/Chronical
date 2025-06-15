# statistic/views.py

from django.shortcuts import render, get_object_or_404
from .models import StatisticalChapter

def statistical_chapter_detail(request, state_slug, district_slug, chapter_slug):
    # Fetch the chapter, pre-fetching the polymorphic content blocks for efficiency
    chapter = get_object_or_404(
        StatisticalChapter.objects.select_related('district__state'),
        district__state__slug=state_slug,
        district__slug=district_slug,
        slug=chapter_slug
    )

    # The content_blocks related manager will fetch all block types correctly
    context = {
        'chapter': chapter,
    }
    return render(request, 'statistic/statistical_chapter_detail.html', context)