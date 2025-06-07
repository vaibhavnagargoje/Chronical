from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import State, District, DistrictSVG



def index(request):
    """
    Display the homepage with a list of all States.
    """
    
    return render(request, 'home/index.html',)


def state_detail(request, state_slug):
    """
    Display information about a State and its Districts.
    """
    state = get_object_or_404(State, slug=state_slug)
    districts = state.districts.all()  # All districts in this state
    
    # Get SVG content for districts in this state
    district_svgs = DistrictSVG.objects.filter(district__state=state)
    
    context = {
        'state': state,
        'districts': districts,
        'district_svgs': district_svgs,
    }
    return render(request, 'home/state_detail.html', context)


def district_detail(request, state_slug, district_slug):
    """
    Display information about a particular District, including its introduction.
    """
    state = get_object_or_404(State, slug=state_slug)
    district = get_object_or_404(state.districts, slug=district_slug)
    cultural_chapters_qs = district.cultural_chapters.all().order_by('name')

    # statistical_chapters_qs = district.statistical_chapters.all().order_by('name')   # Uncomment if you have statistical chapters
    
    # Get related data with prefetch_related for optimization
    district_images = district.images.all()
    district_paragraphs = district.paragraphs.all()
    district_quick_facts = district.quick_facts.all()
    district_sections = district.sections.all().prefetch_related('paragraphs', 'images')
    
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
            'People': {'icon': 'people.png', 'desc': 'Demographics and communities'},
            'Political History': {'icon': 'political_history.png', 'desc': 'Maratha Empire to modern times'},
            'Sports & Games': {'icon': 'sports_games.png', 'desc': 'Traditional and modern sports'},
            'Stories': {'icon': 'stories.png', 'desc': 'Folk tales and local narratives'},
        },
        'Statistical': {
            'Agriculture': {'icon': 'agriculture.png', 'desc': 'Farming practices and crops'},
            'Demography': {'icon': 'demography.png', 'desc': 'Population and social statistics'},
            'Education': {'icon': 'education.png', 'desc': 'Schools and higher education'},
            'Environment': {'icon': 'environment.png', 'desc': 'Climate and ecological data'},
            'Health': {'icon': 'health.png', 'desc': 'Medical facilities and wellness'},
            'Industry': {'icon': 'industry.png', 'desc': 'IT, automotive, manufacturing'},
            'Labour': {'icon': 'labour.png', 'desc': 'Employment and workforce data'},
            'Livestock & Fisheries': {'icon': 'livestock_fisheries.png', 'desc': 'Animal husbandry and aquaculture'},
            'Police & Judiciary': {'icon': 'police_judiciary.png', 'desc': 'Law enforcement and justice system'},
            'Revenue & Expenditure': {'icon': 'revenue.png', 'desc': 'Financial and budget data'},
            'Transport & Communication': {'icon': 'transcomm.png', 'desc': 'Infrastructure and connectivity'},
        }
    }
    
    cultural_chapters_list = []
    for chapter in cultural_chapters_qs:
        meta = CHAPTER_META['Cultural'].get(chapter.name, {}) # Use .get for safety
        cultural_chapters_list.append({
            'object': chapter,
            'icon': meta.get('icon', 'default.png'), # default icon if not found
            'desc': meta.get('desc', 'No description available.'),
        })
        
    # statistical_chapters_list = []
    # for chapter in statistical_chapters_qs:
    #     meta = CHAPTER_META['Statistical'].get(chapter.name, {})
    #     statistical_chapters_list.append({
    #         'object': chapter,
    #         'icon': meta.get('icon', 'default.png'),
    #         'desc': meta.get('desc', 'No description available.'),
    #     })



    context = {
        'state': state,
        'district': district,
        'cultural_chapters': cultural_chapters_list, # Pass the new processed list
        'district_images': district_images,
        'district_paragraphs': district_paragraphs,
        'district_quick_facts': district_quick_facts,
        'district_sections': district_sections,
        
    }
    return render(request, 'home/district_detail.html', context)

