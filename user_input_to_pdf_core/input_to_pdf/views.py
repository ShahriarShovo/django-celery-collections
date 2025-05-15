from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .tasks import generate_pdf_from_form
from celery.result import AsyncResult


# Create your views here.
# form submission view
@api_view(['POST'])
def submit_form(request):
    #getting input from user information
    data = {
        "fname": request.data.get('fname'),
        "lname": request.data.get('lname'),
        "email": request.data.get('email'),
        "age": request.data.get('age'),
        "university": request.data.get('university'),
        "address": request.data.get('address'),
    }
    #send user data to celery for background processing
    task = generate_pdf_from_form.delay(**data)
    
    # return status
    return Response({
        "message": "Form submitted successfully. PDF generation started.",
        "task_id": task.id
    })

#Celery backend processing result view
@api_view(['GET'])
def check_pdf_status_view(request, task_id):
    #create new result and pass task id
    result = AsyncResult(task_id)
    #if state is success,it will return pdf file link
    if result.state == 'SUCCESS':
        return Response({"pdf_url": result.result})
    #else it will show a state or error
    else:
        return Response({"status": result.state})
        
