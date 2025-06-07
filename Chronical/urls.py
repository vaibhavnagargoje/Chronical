# your_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- FIX: Put specific app URLs FIRST ---
    # Django will now check for '/search/' and '/cultural/' before trying the generic home patterns.
    path('search/', include('search.urls', namespace='search')),
    path('cultural/', include('culture.urls', namespace='culture')),
    path('statistical/', include('statistic.urls')), # Also adding namespace for best practice

    # --- The generic home URL pattern now comes LAST ---
    # This will act as a "catch-all" for URLs that didn't match the specific apps above.
    path('', include('home.urls', namespace='home')),
]

# For serving media files in development (only):
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)