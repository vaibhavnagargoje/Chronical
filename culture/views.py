# culture/views.py

from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from itertools import chain
from .models import CulturalChapter, HeadingBlockOne, HeadingBlockTwo, ParagraphBlock, ImageBlock, ReferenceBlock

def cultural_chapter_detail(request, state_slug, district_slug, chapter_slug):
    """
    A robust view that manually fetches all subclassed content blocks to ensure
    it works with any version of django-polymorphic.
    """
    chapter = get_object_or_404(
        CulturalChapter.objects.select_related('district__state'),
        slug=chapter_slug,
        district__slug=district_slug,
        district__state__slug=state_slug
    )

    # --- NEW, ROBUST LOGIC TO GET CONTENT BLOCKS ---
    # We will fetch each type of block separately as a standard Django queryset.
    h1s = HeadingBlockOne.objects.filter(chapter=chapter)
    h2s = HeadingBlockTwo.objects.filter(chapter=chapter)
    paras = ParagraphBlock.objects.filter(chapter=chapter)
    imgs = ImageBlock.objects.filter(chapter=chapter)
    refs = ReferenceBlock.objects.filter(chapter=chapter)

    # Combine all the querysets into a single list.
    # The `chain` function from `itertools` is efficient for this.
    all_blocks_list = list(chain(h1s, h2s, paras, imgs, refs))

    # Manually sort the combined list by the 'order' attribute.
    all_blocks_list.sort(key=lambda x: x.order)
    
    # We now have the correctly typed and ordered blocks in `all_blocks_list`.
    # Let's rename it for consistency with the rest of the code.
    content_blocks = all_blocks_list

    # --- The rest of the view logic is the same and already correct ---
    # It relies on `content_blocks` being a list of correctly-typed subclass objects.

    # Generate the Table of Contents from the heading blocks
    table_of_contents = []
    for block in content_blocks:
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