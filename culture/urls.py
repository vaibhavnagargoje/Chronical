from django.urls import path
from . import views

app_name = 'culture' # ADD THIS for best practice

urlpatterns = [
    path(
        '<slug:state_slug>/<slug:district_slug>/<slug:chapter_slug>/',
        views.cultural_chapter_detail,
        name='cultural_chapter_detail'
    ),
]