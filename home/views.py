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
    context = {
        'state': state,
        'district': district,
    }
    return render(request, 'home/district_detail.html', context)
