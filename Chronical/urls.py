# your_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
     path('tinymce/', include('tinymce.urls')),

    path('editor/', include('editor.urls', namespace='editor')),
    path('search/', include('search.urls', namespace='search')),
    path('cultural/', include('culture.urls', namespace='culture')),
    path('statistical/', include('statistic.urls')), # Also adding namespace for best practice

    
    path('', include('home.urls', namespace='home')),

    #  #last for reloading bcz its to heavy path
    # path("__reload__/", include("django_browser_reload.urls")),
]

# For serving media files in development (only):
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)