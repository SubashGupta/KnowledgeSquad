from django.contrib import admin
from django.urls import path, include
from django.conf import settings  #this is added as we are user uploaded media needs to be considered.
from django.conf.urls.static import static #in the settings.py we are getting the media url and the media path in the static method.


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('corecode.urls')),
    path('api/', include('corecode.api.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) #meaning, we are showing the media using the media_url path and then collecting the media from the media_root path.