from django.urls import path
from . import views

app_name = 'charthandler'

urlpatterns = [
    path(
        'chart-data/<slug:template_slug>/',
        views.chart_data_api,
        name='chart-data'
    ),
]
