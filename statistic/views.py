# statistic/views.py

from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.http import HttpResponse
# Import the models from the statistic app
from .models import StatisticalChapter, StatisticContentBlock, HeadingBlockOne, HeadingBlockTwo, HeadingBlockThree,ChartBlock
from culture.models import CulturalChapter
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import login_required
import os
from sidepanal.models import SidePanelTerm


@login_required
def statistical_chapter_detail(request, state_slug, district_slug, chapter_slug):
    # Fetch the correct StatisticalChapter using the URL slugs
    chapter = get_object_or_404(
        StatisticalChapter.objects.select_related('district__state'),
        slug=chapter_slug,
        district__slug=district_slug,
        district__state__slug=state_slug
    )

    # Fetch all the polymorphic content blocks for this chapter
    content_blocks = StatisticContentBlock.objects.filter(chapter=chapter)

    # Generate Table of Contents from heading blocks
    table_of_contents = []
    
    for block in content_blocks: # .select_subclasses() is efficient
       
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

        # Uncomment this if you have HeadingBlockThree in Table of contents   
        elif isinstance(block, HeadingBlockThree):
             table_of_contents.append({
                'text': block.text,
                'slug': slugify(block.text),
                'level': 3,
            })

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
        'side_panel_data': side_panel_data, # Pass the data to the template
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
        html_content = chart_block.chart_html_file.read().decode('utf-8')
        
        # Replace relative logo.png with static file URL
        logo_url = static('logo.png')
        # Build absolute URL for iframe context
        logo_absolute_url = request.build_absolute_uri(logo_url)
        html_content = html_content.replace('src="logo.png"', f'src="{logo_absolute_url}"')
        
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
