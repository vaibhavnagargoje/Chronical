# editor/urls.py
from django.urls import path
from . import views

app_name = 'editor'

urlpatterns = [
    # select which chapter to edit
    path('culture/', views.select_chapter_view, name='select_chapter'),

    # editor page 
    path('culture/edit/<int:chapter_id>/', views.chapter_editor_view, name='chapter_editor'),
]