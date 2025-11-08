from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import State, District, DistrictSVG
from sidepanal.models import SidePanelTerm


def index(request):
    """
    Display the homepage with a list of all States.
    """
    # Get all states with their districts for the search dropdown
    all_states = State.objects.prefetch_related('districts').all().order_by('name')
    
    # Get Maharashtra as the featured state (or first state if Maharashtra doesn't exist)
    try:
        featured_state = State.objects.get(slug='maharashtra')
    except State.DoesNotExist:
        featured_state = State.objects.first()
    
    featured_districts = featured_state.districts.all() if featured_state else []
    
    # Meta information for social sharing
    meta = {
        'title': 'The Districts Project',
        'description': 'A comprehensive resource on district-level cultures and statistics of India. Explore and tell us more!', 
        'image': request.build_absolute_uri('/static/img/cka.png'),  # Use your site logo or featured imaget
        'url': request.build_absolute_uri(),
        'type': 'website'
    }
    
    context = {
        'state': featured_state,
        'districts': featured_districts,
        'all_states': all_states,
        'meta': meta,
    }

    return render(request, 'home/index.html', context)


def state_detail(request, state_slug):
    """
    Display information about a State and its Districts.
    """
    state = get_object_or_404(State, slug=state_slug)
    districts = state.districts.all()
    
    # Get SVG content for districts in this state
    district_svgs = DistrictSVG.objects.filter(district__state=state)
    
    # Get all states with their districts for the nested dropdown
    all_states = State.objects.prefetch_related('districts').all().order_by('name')
    
    # Meta information for social sharing
    meta = {
        'title': f'{state.name} The Districts Project | Maharashtra',
        'description': f'A comprehensive resource on district-level cultures and statistics of {state.name}. Explore and tell us more!',
        'image': request.build_absolute_uri('/static/img/cka.png'),  # You can add state-specific images later
        'url': request.build_absolute_uri(),
        'type': 'website'
    }
    
    context = {
        'state': state,
        'districts': districts,
        'district_svgs': district_svgs,
        'all_states': all_states,
        'meta': meta,
    }
    return render(request, 'home/state_detail.html', context)


def district_detail(request, state_slug, district_slug):
    """
    Display information about a particular District, including its introduction.
    """
    state = get_object_or_404(State, slug=state_slug)
    district = get_object_or_404(state.districts, slug=district_slug)
    all_districts_in_state = state.districts.all()
    cultural_chapters_qs = district.cultural_chapters.all().order_by('name')

    statistical_chapters_qs = district.statistical_chapters.all().order_by('name')
    
    # Get related data with prefetch_related for optimization
    district_images = district.images.all()
    district_paragraphs = district.paragraphs.all()
    district_quick_facts = district.quick_facts.all()
    district_gif_images = district.gif_images.all()
    all_terms = SidePanelTerm.objects.all()
    
    final_definitions = {term.term: term.default_definition for term in all_terms}
    
    # Get featured image for social sharing
    featured_image_url = request.build_absolute_uri('/static/img/cka.png')  # default
    if district_images.exists():
        # Use the first district image if available
        featured_image_url = request.build_absolute_uri(district_images.first().webp_medium.url)
    
    # Meta information for social sharing
    meta = {
        'title': f'{district.name} District, {state.name} - Culture & Statistics | The Districts Project',
        'description': f'Cultures and statistics of {district.name} district. Explore and tell us more!',
        'image': featured_image_url,
        'url': request.build_absolute_uri(),
        'type': 'website'
    }

    CHAPTER_META = {
        'Cultural': {
            'Architecture': {'icon': 'architecture.png', 'desc': 'Historical and modern structures'},
            'Artforms': {'icon': 'artforms.png', 'desc': 'Traditional and contemporary arts'},
            'Cultural Sites': {'icon': 'cultural_sites.png', 'desc': 'Museums, temples, and heritage sites'},
            'Festivals & Fairs': {'icon': 'fair_festivals.png', 'desc': 'Ganpati and local celebrations'},
            'Food': {'icon': 'food.png', 'desc': 'Maharashtrian delicacies'},
            'Language': {'icon': 'languages.png', 'desc': 'Marathi and linguistic heritage'},
            'Local Politics': {'icon': 'local_politics.png', 'desc': 'Governance and civic affairs'},
            'Markets': {'icon': 'market.png', 'desc': 'Traditional bazaars and commerce'},
            'History': {'icon': 'history.png', 'desc': 'Maratha Empire to modern times'},
            'Sports & Games': {'icon': 'sports_games.png', 'desc': 'Traditional and modern sports'},
            'Stories': {'icon': 'stories.png', 'desc': 'Folk tales and local narratives'},
        },
        'Statistical': {
            'Agriculture': {'icon': 'agriculture.png', 'desc': 'Farming practices and crops'},
            'Demography': {'icon': 'demography.png', 'desc': 'Population and social statistics'},
            'Education': {'icon': 'education.png', 'desc': 'Schools and higher education'},
            'Elections': {'icon': 'elections.png', 'desc': 'Voting and electoral processes'},
            'Environment': {'icon': 'environment.png', 'desc': 'Climate and ecological data'},
            'Health': {'icon': 'health.png', 'desc': 'Medical facilities and wellness'},
            'Industry': {'icon': 'industry.png', 'desc': 'IT, automotive, manufacturing'},
            'Labor': {'icon': 'labor.png', 'desc': 'Employment and workforce data'},
            'Livestock & Fisheries': {'icon': 'livestock_fisheries.png', 'desc': 'Animal husbandry and aquaculture'},
            'Police & Judiciary': {'icon': 'police_judiciary.png', 'desc': 'Law enforcement and justice system'},
            'Revenue & Expenditure': {'icon': 'revenue.png', 'desc': 'Financial and budget data'},
            'Transport & Communication': {'icon': 'transcomm.png', 'desc': 'Infrastructure and connectivity'},
        }
    }
    
    cultural_chapters_list = []
    for chapter in cultural_chapters_qs:
        meta_info = CHAPTER_META['Cultural'].get(chapter.name, {})
        cultural_chapters_list.append({
            'object': chapter,
            'icon': meta_info.get('icon', 'default.png'),
            'desc': meta_info.get('desc', 'No description available.'),
        })

    statistical_chapters_list = []
    for chapter in statistical_chapters_qs:
        meta_info = CHAPTER_META['Statistical'].get(chapter.name, {})
        statistical_chapters_list.append({
            'object': chapter,
            'icon': meta_info.get('icon', 'default.png'),
            'desc': meta_info.get('desc', 'No description available.'),
        })

    context = {
        'state': state,
        'district': district,
        'cultural_chapters': cultural_chapters_list,
        'statistical_chapters': statistical_chapters_list,
        'district_images': district_images,
        'district_paragraphs': district_paragraphs,
        'district_quick_facts': district_quick_facts,
        'district_gif_images': district_gif_images,
        'all_districts_in_state': all_districts_in_state,
        'side_panel_data': final_definitions,
        'meta': meta,
    }
    return render(request, 'home/district_detail.html', context)


def people(request):
    return render(request, 'home/people.html')