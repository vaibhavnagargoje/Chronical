from django.urls import path
from .views import statistical_chapter_detail

urlpatterns = [
    # e.g. /statistical/maharashtra/kolhapur/demography/
    path('<slug:state_slug>/<slug:district_slug>/<slug:chapter_slug>/',
         statistical_chapter_detail,
         name='statistical_chapter_detail'),
]
