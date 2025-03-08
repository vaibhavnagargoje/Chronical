from django.urls import path
from .views import cultural_chapter_detail

urlpatterns = [
    # e.g. /cultural/maharashtra/kolhapur/food/
    path('<slug:state_slug>/<slug:district_slug>/<slug:chapter_slug>/',
         cultural_chapter_detail,
         name='cultural_chapter_detail'),
]
