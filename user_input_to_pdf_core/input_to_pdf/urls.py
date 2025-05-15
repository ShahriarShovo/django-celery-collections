from django.urls import path
from .views import submit_form, check_pdf_status_view

urlpatterns = [
    path('submit-form/', submit_form),
    path('check-status/<str:task_id>/', check_pdf_status_view),
]