from django.urls import path
from .views import people, careers, disclaimer, partnerships, projects, subscribe, terms

app_name = 'footersection'

urlpatterns = [
    path('people/',people, name='people'),
    path('careers/', careers, name='careers'),
    path('disclaimer/', disclaimer, name='disclaimer'),
    path('partnerships/', partnerships, name='partnerships'),
    path('projects/', projects, name='projects'),
    path('subscribe/', subscribe, name='subscribe'),
    path('terms/', terms, name='terms'),

]