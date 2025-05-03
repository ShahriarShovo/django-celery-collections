from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_verification_email(email, token):
    print("Task started")  # Debug line
    link = f"http://localhost:8000/api/verify-email?email={email}&token={token}"
    print("Verification link:", link)  # Debug line
    message = f"Click here to verify your email {link}"
    try:
        send_mail('Verify your email', message, 'no-reply@site.com', [email], fail_silently=False)
        print("Email sent successfully")
    except Exception as e:
        print("Error sending email:", str(e))
