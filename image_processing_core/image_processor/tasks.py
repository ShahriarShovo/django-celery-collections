# from celery import shared_task, states
# from celery.exceptions import Ignore
# from PIL import Image, ImageDraw, ImageFont
# import os
# from django.conf import settings
# from .models import ImageTask

# @shared_task(bind=True)
# def process_image_task(self, image_path, obj_id):
#     try:
#         #update status
#         self.update_state(states='STARTED')
#         #open Image
#         image_full_path = os.path.join(settings.MEDIA_ROOT, image_path)
#         img = Image.open(image_full_path)
#         #Resize 
#         img = img.resize((500,500))
#         #add water mark
#         draw = ImageDraw.Draw(img)
#         draw.text((10,10), "My Watermark", file = 'white')
#         #saved processed image
#         processed_path = f'processed/{os.path.basename(image_path)}'
#         processed_full_path = os.path.join(settings.MEDIA_ROOT, processed_path)
#         img.save(processed_full_path)
#         #update model
#         obj = ImageTask.objects.get(id=obj_id)
#         obj.processed_image = processed_path
#         obj.status = "SUCCESS"
#         obj.save()
#         return 'Done'
        
#     except Exception as e:
#         self.update_state(state= states.FAILURE, meta ={'error', str(e)})
#         obj = ImageTask.objects.get(id=obj_id)
#         obj.status = 'FAILURE'
#         obj.save()
#         raise Ignore()
        
        
from celery import shared_task, states
from celery.exceptions import Ignore
from PIL import Image, ImageDraw, ImageFont
import os
from django.conf import settings
from .models import ImageTask
import base64

# def encode_image_to_base64(image_path):
#     with open(image_path, "rb") as img_file:
#         return base64.b64encode(img_file.read()).decode('utf-8')

def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except Exception as e:
        raise ValueError(f"Error encoding image to base64: {str(e)}")


@shared_task(bind=True)
def process_image_task(self, image_path, obj_id):
    try:
        # Update status
        self.update_state(states='STARTED')

        # Open Image
        image_full_path = os.path.join(settings.MEDIA_ROOT, image_path)
        img = Image.open(image_full_path)

        # Resize
        img = img.resize((500, 500))

        # Add watermark
        draw = ImageDraw.Draw(img)
        draw.text((10, 10), "My Watermark", fill='white')

        # Save processed image
        processed_path = f'processed/{os.path.basename(image_path)}'
        processed_full_path = os.path.join(settings.MEDIA_ROOT, processed_path)
        img.save(processed_full_path)

        # Encode processed image to base64 and save it in the model
        encoded_image = encode_image_to_base64(processed_full_path)

        # Update model
        obj = ImageTask.objects.get(id=obj_id)
        obj.processed_image = processed_path
        obj.encoded_processed_image = encoded_image  # Save the base64 encoded image
        obj.status = "SUCCESS"
        obj.save()

        return 'Done'

    except Exception as e:
        self.update_state(state=states.FAILURE, meta={'error': str(e)})
        obj = ImageTask.objects.get(id=obj_id)
        obj.status = 'FAILURE'
        obj.save()
        raise Ignore()
