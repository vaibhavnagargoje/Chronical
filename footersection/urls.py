from django.urls import path
from .views import people, careers, disclaimer, partnerships, projects, subscribe, terms

app_name = 'footersection'

urlpatterns = [
    path('people/',people, name='people'),
    path('careers/', careers, name='careers'),
    path('disclaimer/', disclaimer, name='disclaimers'),
    path('partnerships/', partnerships, name='partnership'),
    path('projects/', projects, name='project'),
    path('subscribe/', subscribe, name='subscribe'),
    path('terms/', terms, name='terms'),

]