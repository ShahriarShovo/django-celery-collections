from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from .tasks import convert_image_to_pdf_task
from celery.result import AsyncResult
import os 
from django.http import FileResponse, Http404


#home page
def index(request):
    return render(request, 'converter/index.html')

#image upload function
def upload_images(request):
    #request file(image) with post
    if request.method == 'POST':
        #getting file from html template
        files = request.FILES.getlist('file')
        #if there is not file upload or empty, it will return json response
        if not files:
            return JsonResponse({'success':False, 'error': 'no file uploaded'})
        
        #created path where image will saved
        image_dir = os.path.join(settings.MEDIA_ROOT, 'images')
        #if there is not path than create on path, if path already exist than handle error with exist_ok
        os.makedirs(image_dir, exist_ok=True)
        file_paths = [] # here all file path will save
        for file in files:
            file_path = os.path.join(image_dir, file.name) # created every files full path
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk) # write chunk by chunk
                file_paths.append(file_path) # use file for next step 
        #send file paths to celery
        result = convert_image_to_pdf_task.delay(file_paths)
        #save task id in session as if it will track later
        request.session['task_id'] = result.id
        return JsonResponse({'success':True})
    # if not post than error
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'})
    
#showing a html page while creating pdf
def pdf_generation_in_progress(request):
    return render(request, 'converter/pdf_generation_in_progress.html')


def get_generated_pdf(request):
    task_id = request.session.get('task_id')
    if not task_id:
        return redirect('index')

    task_result = AsyncResult(task_id)

    pdf_output_path = os.path.join(settings.MEDIA_ROOT, 'pdf', 'output.pdf')

    if task_result.status == 'SUCCESS' and os.path.exists(pdf_output_path):
        try:
            return FileResponse(
                open(pdf_output_path, 'rb'),
                as_attachment=True,
                filename='output.pdf',
                content_type='application/pdf'
            )
        except FileNotFoundError:
            raise Http404("PDF not found.")
    else:
        return render(request, 'converter/pdf_generation_in_progress.html')

    
    

        
