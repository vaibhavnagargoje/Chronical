# statistic/views.py

from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.http import HttpResponse
# Import the models from the statistic app
from .models import StatisticalChapter, StatisticContentBlock, HeadingBlockOne, HeadingBlockTwo, HeadingBlockThree, ChartBlock, ReferenceBlock, ImageBlock
from culture.models import CulturalChapter
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import login_required
import os
import re
from sidepanal.models import SidePanelTerm



def statistical_chapter_detail(request, state_slug, district_slug, chapter_slug):
    # Fetch the correct StatisticalChapter using the URL slugs
    chapter = get_object_or_404(
        StatisticalChapter.objects.select_related('district__state'),
        slug=chapter_slug,
        district__slug=district_slug,
        district__state__slug=state_slug
    )

    # # Fetch all the polymorphic content blocks for this chapter
    # content_blocks = StatisticContentBlock.objects.filter(chapter=chapter)
    # Fetch all the polymorphic content blocks for this chapter
    content_blocks_qs = StatisticContentBlock.objects.filter(chapter=chapter)
    content_blocks = list(content_blocks_qs)
    reference_blocks = sorted(
        (block for block in content_blocks if isinstance(block, ReferenceBlock)),
        key=lambda block: (block.text or '').lower()
    )
    non_reference_blocks = [block for block in content_blocks if not isinstance(block, ReferenceBlock)]
    content_blocks = non_reference_blocks + reference_blocks
    # Generate Table of Contents from heading blocks
    table_of_contents = []
    
    num=0
    for block in content_blocks: # .select_subclasses() is efficient
        if isinstance(block, HeadingBlockOne):
            anchor_slug = f"{slugify(block.text)}-{num}"
            block.anchor_slug = anchor_slug
            table_of_contents.append({
                'text': block.text,
                'slug': anchor_slug,
                'level': 1,
            })
            num+=1
        elif isinstance(block, HeadingBlockTwo):
            anchor_slug = f"{slugify(block.text)}-{num}"
            block.anchor_slug = anchor_slug
            table_of_contents.append({
                'text': block.text,
                'slug': anchor_slug,
                'level': 2,
            })
            num+=1
        # Uncomment this if you have HeadingBlockThree in Table of contents   
        elif isinstance(block, HeadingBlockThree):
             anchor_slug = f"{slugify(block.text)}-{num}"
             block.anchor_slug = anchor_slug
             table_of_contents.append({
                'text': block.text,
                'slug': anchor_slug,
                'level': 3,
            })
             num+=1
        elif isinstance(block, ChartBlock):
            chart_title = _ensure_chart_title(block)
            if chart_title:
                anchor_slug = f"{slugify(chart_title)}-{num}"
                block.anchor_slug = anchor_slug
                table_of_contents.append({
                    'text': chart_title,
                    'slug': anchor_slug,
                    'level': 3,
                })
                num+=1

    # Get all chapters in the current district for the "Change Chapter" dropdown
    # Note the use of the `related_name` 'statistical_chapters'
    all_chapters_in_district = chapter.district.statistical_chapters.all().order_by('name')
    all_cultural_chapters_in_district = chapter.district.cultural_chapters.all().order_by('name')

    # Get all districts in the current state for the "Change District" dropdown
    all_districts_in_state = chapter.district.state.districts.all().order_by('name')
    side_panel_data = get_definitions_for_chapter(chapter, 'statistic')


    # Get Previous and Next Chapters for bottom navigation
    chapter_list = list(all_chapters_in_district)
    try:
        current_index = chapter_list.index(chapter)
        prev_chapter = chapter_list[current_index - 1] if current_index > 0 else None
        next_chapter = chapter_list[current_index + 1] if current_index < len(chapter_list) - 1 else None
    except ValueError:
        # This case handles if the chapter isn't found in the list, though it should be.
        current_index, prev_chapter, next_chapter = -1, None, None

    # Get featured image for social sharing
    featured_image_url = request.build_absolute_uri('/static/img/cka.png')  # default
    image_blocks = [block for block in content_blocks if isinstance(block, ImageBlock)]
    if image_blocks:
        # Use the first image in the chapter
        # featured_image_url = request.build_absolute_uri(image_blocks[0].webp_medium.url)
        featured_image_url = request.build_absolute_uri('/static/img/cka.png')

    # Meta information for social sharing
    meta = {
        'title': f'{chapter.name}: {chapter.district.name}, {chapter.district.state.name} | The Districts Project',
        'description': f'Explore {chapter.name} in {chapter.district.name} district.',
        'image': featured_image_url,
        'url': request.build_absolute_uri(),
        'type': 'article'
    }

    context = {
        'state': chapter.district.state,
        'district': chapter.district,
        'chapter': chapter,
        'content_blocks': content_blocks,
        'table_of_contents': table_of_contents,
        'all_chapters_in_district': all_chapters_in_district,
        'all_cultural_chapters_in_district': all_cultural_chapters_in_district,
        'all_districts_in_state': all_districts_in_state,
        'prev_chapter': prev_chapter,
        'next_chapter': next_chapter,
        'side_panel_data': side_panel_data,
        'meta': meta,
    }
    
    # Render the response using a new template for the statistic detail page
    return render(request, 'statistic/chapter_detail.html', context)


@xframe_options_exempt
def serve_chart_html(request, chart_block_id):
    """
    This view finds a ChartBlock by its ID, reads its associated HTML file,
    and returns it as an HTTP response that can be safely embedded in an iframe.
    """
    from django.templatetags.static import static
    
    chart_block = get_object_or_404(ChartBlock, pk=chart_block_id)
    try:
        with chart_block.chart_html_file.open('rb') as chart_file:
            raw_html = chart_file.read().decode('utf-8', errors='ignore')
        extracted_title = _extract_chart_title(raw_html)
        if extracted_title and chart_block.title != extracted_title:
            chart_block.title = extracted_title
            chart_block.save(update_fields=['title'])
        logo_url = static('logo.png')
        logo_absolute_url = request.build_absolute_uri(logo_url)
        html_content = raw_html.replace('src="logo.png"', f'src="{logo_absolute_url}"')
        return HttpResponse(html_content, content_type='text/html')
    except Exception as e:
        return HttpResponse("<h1>Chart file not found.</h1>", status=404, content_type='text/html')



def get_definitions_for_chapter(chapter_instance, chapter_type):
    """
    Helper function to get the final, context-aware dictionary of definitions.
    """
    all_terms = SidePanelTerm.objects.all()
    # 1. Start with all default definitions. Use the original term case for the key.
    final_definitions = {term.term: term.default_definition for term in all_terms}

    # 2. Find overrides for this specific chapter
    if chapter_type == 'culture':
        context_filter = {'cultural_chapter': chapter_instance}
    else: # statistic
        context_filter = {'statistical_chapter': chapter_instance}

    contextual_defs = chapter_instance.contextual_definitions.select_related('term').all()

    # 3. Apply the overrides
    for c_def in contextual_defs:
        term_key = c_def.term.term
        if not c_def.is_active:
            # If marked inactive, remove it from the final list
            if term_key in final_definitions:
                del final_definitions[term_key]
        elif c_def.override_definition:
            # If an override exists, use it
            final_definitions[term_key] = c_def.override_definition
            
    return final_definitions


def _extract_chart_title(html_content):
    match = re.search(r'<title>\s*(.*?)\s*</title>', html_content, flags=re.IGNORECASE | re.DOTALL)
    return re.sub(r'\s+', ' ', match.group(1)).strip() if match else None

def _ensure_chart_title(block):
    try:
        with block.chart_html_file.open('rb') as chart_file:
            html_content = chart_file.read().decode('utf-8', errors='ignore')
    except Exception:
        return None
    extracted_title = _extract_chart_title(html_content)
    if extracted_title and block.title != extracted_title:
        block.title = extracted_title
        block.save(update_fields=['title'])
    return block.title
