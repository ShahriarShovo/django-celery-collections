from django.urls import path
from .views import register_view, verify_email_view, resend_otp_view


urlpatterns = [
    path('register/', register_view),
    path('verify-email/', verify_email_view),
    path('resend-token/', resend_otp_view),
]