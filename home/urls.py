from django.urls import path
from .views import state_detail, district_detail, index

app_name = 'home'

urlpatterns = [
    path('',index, name='index'),
    #  /maharashtra/
    path('<slug:state_slug>/', state_detail, name='state_detail'),

    #   /maharashtra/kolhapur/
    path('<slug:state_slug>/<slug:district_slug>/', district_detail, name='district_detail'),
]
