from django.urls import path
from .views import people, careers, disclaimer, partnerships, projects, subscribe, terms, edit_project, edit_partnership, edit_careers, edit_terms, edit_disclaimer

app_name = 'footersection'

urlpatterns = [
    path('people/',people, name='people'),
    path('careers/', careers, name='careers'),
    path('careers/edit/', edit_careers, name='edit_careers'),
    path('disclaimer/', disclaimer, name='disclaimers'),
    path('disclaimer/edit/', edit_disclaimer, name='edit_disclaimer'),
    path('partnerships/', partnerships, name='partnership'),
    path('partnerships/edit/', edit_partnership, name='edit_partnership'),
    path('projects/', projects, name='project'),
    path('projects/edit/', edit_project, name='edit_project'),
    path('subscribe/', subscribe, name='subscribe'),
    path('terms/', terms, name='terms'),
    path('terms/edit/', edit_terms, name='edit_terms'),
]