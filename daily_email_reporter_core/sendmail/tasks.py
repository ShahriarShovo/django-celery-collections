from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_mail_task():
    print("Mail sending.......")
    subject = 'welcome to Celery world'    
    message = 'Hi thank you for using celery'
    #GET mail from settings to send mail
    email_from = settings.EMAIL_HOST_USER
    #get destination email
    recipient_list = ['recipient@mail.com',]
    #send mail with send mail function
    send_mail( subject, message, email_from, recipient_list )    
    return "Mail has been sent........"