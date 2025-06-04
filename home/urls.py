from django.urls import path
from .views import state_detail, district_detail, index

urlpatterns = [
    path('',index, name='index'), 
    # e.g - /maharashtra/
    path('<slug:state_slug>/', state_detail, name='state_detail'),

    # e.g-  /maharashtra/kolhapur/
    path('<slug:state_slug>/<slug:district_slug>/', district_detail, name='district_detail'),
]
