# search/urls.py
from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [
    path('', views.search_view, name='query'),
]