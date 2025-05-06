from django.db import models

# Create your models here.
class ImageTask(models.Model):
    original_image = models.ImageField(upload_to='originals/')
    processed_image = models.ImageField(upload_to='processed/', blank=True, null=True)
    task_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.task_id
    
    
