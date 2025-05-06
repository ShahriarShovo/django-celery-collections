from django.urls import path
from .views import UploadImageView,TaskStatusView

urlpatterns = [
    path('image_view/', UploadImageView.as_view(), name='uploadImageView'),
    path('task_view/<str:task_id>/', TaskStatusView.as_view(), name='task_view'),
]
