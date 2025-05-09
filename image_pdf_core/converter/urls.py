from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_images, name='upload_images'),
    path('pdf_generation_in_progress/', views.pdf_generation_in_progress, name='pdf_generation_in_progress'),
    path('get_generated_pdf/', views.get_generated_pdf, name='get_generated_pdf'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)