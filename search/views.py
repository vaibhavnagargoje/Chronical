# search/views.py

from django.shortcuts import render
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.utils import timezone
from django.utils.text import slugify
from datetime import timedelta
import re

from home.models import District
from culture.models import CulturalChapter, ParagraphBlock, HeadingBlockOne, HeadingBlockTwo

# This is a constant we can use to identify result types
DISTRICT_TYPE = 'District Overview'
CULTURE_TYPE = 'Cultural Chapter'

def search_view(request):
    """
    A comprehensive search view that handles querying, filtering, pagination,
    and facet counting.
    """
    query = request.GET.get('q', '')
    
    # --- Filtering ---
    # Get filter parameters from the URL, e.g., ?content_type=District Overview&state=Maharashtra
    selected_content_types = request.GET.getlist('content_type')
    selected_states = request.GET.getlist('state')
    selected_last_updated = request.GET.get('last_updated')

    # --- Initial Querysets ---
    # We start with base querysets and will filter them down.
    district_results = District.objects.all()
    culture_results = CulturalChapter.objects.all()

    # --- Apply Search Query ('q') ---
    if query:
        # This is a simplified search. For best results, use PostgreSQL Full-Text Search here.
        district_results = district_results.filter(
            Q(name__icontains=query) | Q(introduction__icontains=query)
        )
        culture_results = culture_results.filter(
            Q(name__icontains=query) |
            Q(content_blocks__paragraphblock__content__icontains=query) |
            Q(content_blocks__headingblockone__text__icontains=query)|
            Q(content_blocks__headingblocktwo__text__icontains=query)
        ).distinct() # Added distinct() to avoid duplicate chapters if query matches multiple blocks
        
    # --- Facet Counting (BEFORE filtering) ---
    # We need to count how many results exist for each filter option based on the initial query.
    # This populates the numbers like "Districts (12)" in the sidebar.
    facets = {
        'content_types': {
            DISTRICT_TYPE: district_results.count(),
            CULTURE_TYPE: culture_results.count(),
            # Add counts for other types here
        },
        'states': dict(
            District.objects.filter(id__in=district_results.values_list('id', flat=True))
            .values('state__name')
            .annotate(count=Count('id'))
            .values_list('state__name', 'count')
        )
    }

    # --- Apply Filters from Sidebar ---
    if selected_content_types:
        # If user unchecks "Districts", we make that queryset empty
        if DISTRICT_TYPE not in selected_content_types:
            district_results = district_results.none()
        if CULTURE_TYPE not in selected_content_types:
            culture_results = culture_results.none()

    if selected_states:
        district_results = district_results.filter(state__name__in=selected_states)
        culture_results = culture_results.filter(district__state__name__in=selected_states)

    if selected_last_updated:
        days = 0
        if selected_last_updated == 'week': days = 7
        elif selected_last_updated == 'month': days = 30
        elif selected_last_updated == 'year': days = 365
        
        if days > 0:
            cutoff_date = timezone.now() - timedelta(days=days)
            district_results = district_results.filter(updated_at__gte=cutoff_date)
            culture_results = culture_results.filter(updated_at__gte=cutoff_date)

    # --- Helper function to find matching content and generate anchor ---
    def find_content_anchor(chapter, search_query):
        """Find the specific block containing the search query and return anchor"""
        if not search_query:
            return ''
            
        content_blocks = chapter.content_blocks.select_related().all()
        
        for block in content_blocks:
            model_name = block.polymorphic_ctype.model
            
            if model_name == 'headingblockone':
                heading_block = HeadingBlockOne.objects.get(pk=block.pk)
                if search_query.lower() in heading_block.text.lower():
                    return f"#{slugify(heading_block.text)}"
                    
            elif model_name == 'headingblocktwo':
                heading_block = HeadingBlockTwo.objects.get(pk=block.pk)
                if search_query.lower() in heading_block.text.lower():
                    return f"#{slugify(heading_block.text)}"
                    
            elif model_name == 'paragraphblock':
                paragraph_block = ParagraphBlock.objects.get(pk=block.pk)
                if search_query.lower() in paragraph_block.content.lower():
                    previous_blocks = content_blocks.filter(order__lt=block.order).order_by('-order')
                    for prev_block in previous_blocks:
                        prev_model = prev_block.polymorphic_ctype.model
                        if prev_model in ['headingblockone', 'headingblocktwo']:
                            if prev_model == 'headingblockone':
                                prev_heading = HeadingBlockOne.objects.get(pk=prev_block.pk)
                                return f"#{slugify(prev_heading.text)}"
                            elif prev_model == 'headingblocktwo':
                                prev_heading = HeadingBlockTwo.objects.get(pk=prev_block.pk)
                                return f"#{slugify(prev_heading.text)}"
                    return ''
        return ''

    # --- Helper function to highlight search terms ---
    def highlight_text(text, search_query):
        """Highlight search terms in text"""
        if not search_query or not text:
            return text
        pattern = re.compile(re.escape(search_query), re.IGNORECASE)
        return pattern.sub(f'<mark class="bg-yellow-200 px-1 rounded">{search_query}</mark>', text)

    # --- Combine and Format Results ---
    # We transform our querysets into a unified list of dictionaries for easy rendering.
    final_results = []
    for district in district_results.select_related('state'):
        description = highlight_text(district.introduction, query)
        final_results.append({
            'type': DISTRICT_TYPE,
            'title': highlight_text(f"{district.name} District Overview", query),
            'description': description,
            'url': district.get_absolute_url(),
            'state_name': district.state.name,
            'updated_at': district.updated_at,
        })

    for chapter in culture_results.select_related('district__state').prefetch_related('content_blocks'):
        # Find specific anchor for the matching content
        anchor = find_content_anchor(chapter, query)
        base_url = chapter.get_absolute_url()
        full_url = f"{base_url}{anchor}" if anchor else base_url
        
        # Get description from first paragraph or matching content
        first_paragraph = chapter.content_blocks.instance_of(ParagraphBlock).first()
        description = first_paragraph.content if first_paragraph else "..."
        description = highlight_text(description, query)

        final_results.append({
            'type': CULTURE_TYPE,
            'title': highlight_text(f"{chapter.district.name} - {chapter.name}", query),
            'description': description,
            'url': full_url,
            'state_name': chapter.district.state.name,
            'updated_at': chapter.updated_at,
        })
        
    # --- Sort the combined list (e.g., by update date) ---
    final_results.sort(key=lambda x: x['updated_at'], reverse=True)
    
    # --- Pagination ---
    paginator = Paginator(final_results, 10) # Show 10 results per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'query': query,
        'page_obj': page_obj,
        'total_results': paginator.count,
        'facets': facets,
        'selected_filters': {
            'content_types': selected_content_types,
            'states': selected_states,
            'last_updated': selected_last_updated,
        }
    }
    return render(request, 'search/search_results.html', context)