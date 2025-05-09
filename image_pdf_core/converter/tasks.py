from celery import shared_task
from fpdf import FPDF
import os
from django.conf import settings
import uuid


@shared_task
def convert_image_to_pdf_task(filepaths):
    # Create a new PDF
    pdf = FPDF()
    pdf.set_auto_page_break(0)
    
    # Add each image to a new page
    for filepath in filepaths:
        pdf.add_page()
        pdf.image(filepath, x=10, y=10, w=190)

    # Create the directory if it doesn't exist
    output_dir = os.path.join(settings.MEDIA_ROOT, 'pdf')
    os.makedirs(output_dir, exist_ok=True)

    # Use a unique filename to avoid overwrite/lock issues
    unique_filename = f"{uuid.uuid4().hex}.pdf"
    pdf_output_path = os.path.join(output_dir, unique_filename)

    # Write the PDF to the file
    pdf.output(pdf_output_path)

    # Return relative path to use later
    return os.path.join('pdf', unique_filename)
