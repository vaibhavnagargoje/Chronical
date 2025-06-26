from django.urls import path
from . import views

app_name = 'importdata'

urlpatterns = [
    # Path to import data from a CSV file
    path('import/', views.import_data_view, name='import_data'),
    
]