# # editor/urls.py
# from django.urls import path
# from . import views

# app_name = 'editor'

# urlpatterns = [
#     # select which chapter to edit
#     path('culture/', views.select_chapter_view, name='select_chapter'),

#     # editor page 
#     path('culture/edit/<int:chapter_id>/', views.chapter_editor_view, name='chapter_editor'),
# ]






# editor/urls.py

from django.urls import path
from . import views

app_name = 'editor'

urlpatterns = [
    # The URL now specifies which app's chapters to select from
    # e.g., /editor/culture/ or /editor/statistic/
    path('<str:app_label>/', views.select_chapter_view, name='select_chapter'),

    # The editor URL also specifies the app context
    # e.g., /editor/culture/edit/123/
    path('<str:app_label>/edit/<int:chapter_id>/', views.chapter_editor_view, name='chapter_editor'),
]