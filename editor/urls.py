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

    # suggest edit url (handles both chapters and districts)
    path('<str:app_label>/suggest_edit/<int:chapter_id>/', views.suggest_edit_view, name='suggest_edit'),

    # URL to update review status of a chapter
    path('<str:app_label>/<int:chapter_id>/update-review/', views.update_review_status, name='update_review_status'),

    # District intro editor URL
    path('district/<int:district_id>/intro/', views.district_intro_edit, name='district_intro_edit'),
]