from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ImageTask
from .serializers import ImageTaskSerializer
from .tasks import process_image_task
from celery.result import AsyncResult

# Create your views here.

class UploadImageView(APIView):
    def post(self, request):
        serializer = ImageTaskSerializer(data=request.data)
        
        if serializer.is_valid():
            instance = serializer.save()
            task = process_image_task.delay(instance.original_image.name, instance.id)
            instance.task_id = task.id 
            instance.save()
            return Response({"task_id":task.id, "image_id":instance.id})
        return Response(serializer.errors, status=400)
    
class TaskStatusView(APIView):
    def get(self, request,task_id):
        result = AsyncResult(task_id)
        return Response({"task_id":task_id, "status":result.status})
