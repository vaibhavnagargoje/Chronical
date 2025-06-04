from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import State, District



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
    context = {
        'state': state,
        'districts': districts,
    }
    return render(request, 'home/state_detail.html', context)


def district_detail(request, state_slug, district_slug):
    """
    Display information about a particular District, including its introduction.
    """
    state = get_object_or_404(State, slug=state_slug)
    district = get_object_or_404(state.districts, slug=district_slug)
    
    # Get related data with prefetch_related for optimization
    district_images = district.images.all()
    district_paragraphs = district.paragraphs.all()
    district_quick_facts = district.quick_facts.all()
    district_sections = district.sections.all().prefetch_related('paragraphs', 'images')
    
    context = {
        'state': state,
        'district': district,
        'district_images': district_images,
        'district_paragraphs': district_paragraphs,
        'district_quick_facts': district_quick_facts,
        'district_sections': district_sections,
    }
    return render(request, 'home/district_detail.html', context)
