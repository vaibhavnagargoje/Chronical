# search/views.py

from django.shortcuts import render
from django.db.models import Q, Count, Prefetch
from django.core.paginator import Paginator
from django.utils import timezone
from django.utils.text import slugify
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import asyncio
from functools import lru_cache
from django.db import connection

from home.models import District
from culture.models import CulturalChapter
# Use aliases to resolve model name conflicts
from culture.models import ParagraphBlock as CultureParagraphBlock

from statistic.models import StatisticalChapter
from statistic.models import ParagraphBlock as StatisticParagraphBlock


# This is a constant we can use to identify result types
DISTRICT_TYPE = 'District Overview'
CULTURE_TYPE = 'Cultural Chapter'
STATISTIC_TYPE = 'Statistical Chapter'

# Cache timeouts
SEARCH_CACHE_TIMEOUT = 600  # 10 minutes
COUNT_CACHE_TIMEOUT = 1800  # 30 minutes
QUERY_CACHE_TIMEOUT = 300   # 5 minutes

def get_cache_key(query, selected_content_types, cache_type="search"):
    """Generate cache key for different types of cached data"""
    key_data = {
        'query': query,
        'content_types': sorted(selected_content_types) if selected_content_types else [],
        'type': cache_type
    }
    key_string = json.dumps(key_data, sort_keys=True)
    return f"{cache_type}_{hashlib.md5(key_string.encode()).hexdigest()}"

def get_count_cache_key(model_type, query):
    """Separate cache key for counts only"""
    return get_cache_key(query, [], f"count_{model_type}")

@lru_cache(maxsize=128)
def get_optimized_district_queryset():
    """Cached base queryset for districts"""
    return District.objects.select_related('state').only(
        'id', 'name', 'introduction', 'state__name', 'updated_at'
    )

@lru_cache(maxsize=128)
def get_optimized_culture_queryset():
    """Cached base queryset for cultural chapters"""
    paragraph_prefetch = Prefetch(
        'content_blocks',
        queryset=CultureParagraphBlock.objects.only('content')[:1],
        to_attr='first_paragraphs'
    )
    
    return CulturalChapter.objects.select_related('district__state').prefetch_related(
        paragraph_prefetch
    ).only('id', 'name', 'district__name', 'district__state__name', 'updated_at')

@lru_cache(maxsize=128)
def get_optimized_statistic_queryset():
    """Cached base queryset for statistical chapters"""
    paragraph_prefetch = Prefetch(
        'content_blocks',
        queryset=StatisticParagraphBlock.objects.only('content')[:1],
        to_attr='first_paragraphs'
    )
    
    return StatisticalChapter.objects.select_related('district__state').prefetch_related(
        paragraph_prefetch
    ).only('id', 'name', 'district__name', 'district__state__name', 'updated_at')

def search_districts(query, count_only=False):
    """Optimized district search with count-only option"""
    count_cache_key = get_count_cache_key('district', query)
    
    if count_only:
        cached_count = cache.get(count_cache_key)
        if cached_count is not None:
            return [], cached_count
    
    queryset = get_optimized_district_queryset()
    
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) | Q(introduction__icontains=query)
        )
    
    count = queryset.count()
    cache.set(count_cache_key, count, COUNT_CACHE_TIMEOUT)
    
    if count_only:
        return [], count
    
    # Use iterator for memory efficiency with large datasets
    results = []
    for district in queryset.iterator(chunk_size=100):
        description = district.introduction[:200] + "..." if district.introduction and len(district.introduction) > 200 else (district.introduction or "District overview information")
        results.append({
            'type': DISTRICT_TYPE,
            'title': f"{district.name} District Overview",
            'description': description,
            'url': district.get_absolute_url(),
            'state_name': district.state.name,
            'updated_at': getattr(district, 'updated_at', timezone.now()),
        })
    
    return results, count

def search_cultural_chapters(query, count_only=False):
    """Optimized cultural chapter search with count-only option"""
    count_cache_key = get_count_cache_key('culture', query)
    
    if count_only:
        cached_count = cache.get(count_cache_key)
        if cached_count is not None:
            return [], cached_count
    
    queryset = get_optimized_culture_queryset()
    
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) |
            Q(content_blocks__paragraphblock__content__icontains=query) |
            Q(content_blocks__headingblockone__text__icontains=query) |
            Q(content_blocks__headingblocktwo__text__icontains=query)
        ).distinct()
    
    count = queryset.count()
    cache.set(count_cache_key, count, COUNT_CACHE_TIMEOUT)
    
    if count_only:
        return [], count
    
    results = []
    for chapter in queryset.iterator(chunk_size=100):
        # Get description from prefetched data
        description = "..."
        if hasattr(chapter, 'first_paragraphs') and chapter.first_paragraphs:
            content = chapter.first_paragraphs[0].content
            description = content[:200] + "..." if len(content) > 200 else content
        
        results.append({
            'type': CULTURE_TYPE,
            'title': f"{chapter.district.name} - {chapter.name}",
            'description': description,
            'url': chapter.get_absolute_url(),
            'state_name': chapter.district.state.name,
            'updated_at': chapter.updated_at,
        })
    
    return results, count

def search_statistical_chapters(query, count_only=False):
    """Optimized statistical chapter search with count-only option"""
    count_cache_key = get_count_cache_key('statistic', query)
    
    if count_only:
        cached_count = cache.get(count_cache_key)
        if cached_count is not None:
            return [], cached_count
    
    queryset = get_optimized_statistic_queryset()
    
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) |
            Q(content_blocks__paragraphblock__content__icontains=query) |
            Q(content_blocks__headingblockone__text__icontains=query) |
            Q(content_blocks__headingblocktwo__text__icontains=query)
        ).distinct()
    
    count = queryset.count()
    cache.set(count_cache_key, count, COUNT_CACHE_TIMEOUT)
    
    if count_only:
        return [], count
    
    results = []
    for chapter in queryset.iterator(chunk_size=100):
        description = "..."
        if hasattr(chapter, 'first_paragraphs') and chapter.first_paragraphs:
            content = chapter.first_paragraphs[0].content
            description = content[:200] + "..." if len(content) > 200 else content
        
        results.append({
            'type': STATISTIC_TYPE,
            'title': f"{chapter.district.name} - {chapter.name}",
            'description': description,
            'url': chapter.get_absolute_url(),
            'state_name': chapter.district.state.name,
            'updated_at': chapter.updated_at,
        })
    
    return results, count

def get_facet_counts(query):
    """Get facet counts efficiently using parallel processing"""
    facets_cache_key = get_cache_key(query, [], "facets")
    cached_facets = cache.get(facets_cache_key)
    
    if cached_facets:
        return cached_facets
    
    facets = {'content_types': {}}
    
    # Use concurrent processing for count-only queries
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_to_type = {
            executor.submit(search_districts, query, count_only=True): DISTRICT_TYPE,
            executor.submit(search_cultural_chapters, query, count_only=True): CULTURE_TYPE,
            executor.submit(search_statistical_chapters, query, count_only=True): STATISTIC_TYPE,
        }
        
        for future in as_completed(future_to_type):
            result_type = future_to_type[future]
            try:
                _, count = future.result()
                facets['content_types'][result_type] = count
            except Exception as exc:
                print(f'{result_type} count generated an exception: {exc}')
                facets['content_types'][result_type] = 0
    
    # Cache facets for longer since they change less frequently
    cache.set(facets_cache_key, facets, COUNT_CACHE_TIMEOUT)
    return facets


def search_view(request):
    """
    Highly optimized search view with multi-level caching and efficient concurrency.
    """
    query = request.GET.get('q', '').strip()
    selected_content_types = request.GET.getlist('content_type')
    page_number = request.GET.get('page', 1)
    
    # Multi-level cache strategy
    main_cache_key = get_cache_key(query, selected_content_types)
    cached_result = cache.get(main_cache_key)
    
    if cached_result:
        final_results = cached_result['results']
        facets = cached_result['facets']
    else:
        # Get facets first (might be cached separately)
        facets = get_facet_counts(query)
        
        # Execute searches concurrently only for selected types
        final_results = []
        search_tasks = []
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_type = {}
            
            # Only search for selected content types or all if none selected
            if not selected_content_types or DISTRICT_TYPE in selected_content_types:
                future_to_type[executor.submit(search_districts, query)] = DISTRICT_TYPE
            
            if not selected_content_types or CULTURE_TYPE in selected_content_types:
                future_to_type[executor.submit(search_cultural_chapters, query)] = CULTURE_TYPE
            
            if not selected_content_types or STATISTIC_TYPE in selected_content_types:
                future_to_type[executor.submit(search_statistical_chapters, query)] = STATISTIC_TYPE
            
            # Collect results as they complete
            for future in as_completed(future_to_type):
                result_type = future_to_type[future]
                try:
                    results, _ = future.result()
                    final_results.extend(results)
                except Exception as exc:
                    print(f'{result_type} search generated an exception: {exc}')
        
        # Sort results by relevance and date
        final_results.sort(key=lambda x: x['updated_at'], reverse=True)
        
        # Cache complete results
        cache.set(main_cache_key, {
            'results': final_results,
            'facets': facets
        }, SEARCH_CACHE_TIMEOUT)
    
    # Apply filters after getting cached results
    if selected_content_types:
        final_results = [r for r in final_results if r['type'] in selected_content_types]
    
    # Efficient pagination - cache paginated results per page
    page_cache_key = f"{main_cache_key}_page_{page_number}"
    cached_page = cache.get(page_cache_key)
    
    if cached_page:
        page_obj = cached_page
        total_results = len(final_results)
    else:
        paginator = Paginator(final_results, 10)
        page_obj = paginator.get_page(page_number)
        total_results = paginator.count
        
        # Cache page for shorter time
        cache.set(page_cache_key, page_obj, QUERY_CACHE_TIMEOUT)

    context = {
        'query': query,
        'page_obj': page_obj,
        'total_results': total_results,
        'facets': facets,
        'selected_filters': {
            'content_types': selected_content_types,
        }
    }
    return render(request, 'search/search_results.html', context)