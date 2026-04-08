# your_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('chronical-admin-panel/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),

    path('editor/', include('editor.urls', namespace='editor')),
    path('search/', include('search.urls', namespace='search')),
    path('users/', include('users.urls', namespace='users')),  
    path('cultures/', include('culture.urls', namespace='culture')),
    path('statistics/', include('statistic.urls')), # Also adding namespace for best practice
    path('api/', include('charthandler.urls', namespace='charthandler')),
    path('sidepanal/', include('sidepanal.urls', namespace='sidepanal')),
    path('importdata/', include('importdata.urls', namespace='importdata')),
    path('admindashboard/', include('admindashboard.urls', namespace='admindashboard')),
    path('footersection/', include('footersection.urls', namespace='footersection')),

    
    path('', include('home.urls', namespace='home')),

    # #  #last for reloading bcz its to heavy path
    # path("__reload__/", include("django_browser_reload.urls")),
]

# For serving media files in development (only):
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)