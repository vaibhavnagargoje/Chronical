from django.urls import path
from .views import statistical_chapter_detail,serve_chart_html

app_name = 'statistic'
urlpatterns = [
    # e.g. /statistical/maharashtra/kolhapur/demography/
    path('<slug:state_slug>/<slug:district_slug>/<slug:chapter_slug>/',
         statistical_chapter_detail,
         name='statistical_chapter_detail'),

    path('chart/<int:chart_block_id>/', serve_chart_html, name='serve_chart_html'),
]
