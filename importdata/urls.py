from django.urls import path
from . import views

app_name = 'importdata'

urlpatterns = [
    # Path to import data from a CSV file
    path('import/', views.import_data_view, name='import_data'),
    path('get_chapter_options/', views.get_chapter_options, name='get_chapter_options'),
]