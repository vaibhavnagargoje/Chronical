# culture/views.py

from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from .models import CulturalChapter, ContentBlock, HeadingBlockOne, HeadingBlockTwo

def cultural_chapter_detail(request, state_slug, district_slug, chapter_slug):
    chapter = get_object_or_404(
        CulturalChapter.objects.select_related('district__state'),
        slug=chapter_slug,
        district__slug=district_slug,
        district__state__slug=state_slug
    )

    # CORRECT: Just filter the base model - polymorphic will handle the rest
    content_blocks = ContentBlock.objects.filter(chapter=chapter)

    # Generate Table of Contents
    table_of_contents = []
    for block in content_blocks:
        # This will now work correctly with concrete subclasses
        if isinstance(block, HeadingBlockOne):
            table_of_contents.append({
                'text': block.text,
                'slug': slugify(block.text),
                'level': 1,
            })
        elif isinstance(block, HeadingBlockTwo):
            table_of_contents.append({
                'text': block.text,
                'slug': slugify(block.text),
                'level': 2,
            })
    # Get all chapters in the current district for the "Change Chapter" dropdown
    all_chapters_in_district = chapter.district.cultural_chapters.all().order_by('name')

    # Get all districts in the current state for the "Change District" dropdown
    all_districts_in_state = chapter.district.state.districts.all().order_by('name')

    # Get Previous and Next Chapters for bottom navigation
    chapter_list = list(all_chapters_in_district)
    try:
        current_index = chapter_list.index(chapter)
        prev_chapter = chapter_list[current_index - 1] if current_index > 0 else None
        next_chapter = chapter_list[current_index + 1] if current_index < len(chapter_list) - 1 else None
    except ValueError:
        current_index, prev_chapter, next_chapter = -1, None, None

    # Build the final context dictionary
    context = {
        'state': chapter.district.state,
        'district': chapter.district,
        'chapter': chapter,
        'content_blocks': content_blocks,
        'table_of_contents': table_of_contents,
        'all_chapters_in_district': all_chapters_in_district,
        'all_districts_in_state': all_districts_in_state,
        'prev_chapter': prev_chapter,
        'next_chapter': next_chapter,
    }
    
    return render(request, 'culture/chapter_detail.html', context)