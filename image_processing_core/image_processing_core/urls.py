
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
#from django.conf.urls.static import static, staticfiles_urlpatterns
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('image_processor.urls'))
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
