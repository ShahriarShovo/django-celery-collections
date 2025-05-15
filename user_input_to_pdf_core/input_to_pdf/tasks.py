from celery import shared_task
from django.conf import settings
import os
from fpdf import FPDF

@shared_task(bind=True)
def generate_pdf_from_form(self, **kwargs):
    #user data read
    name = kwargs.get('fname', '') + ' ' + kwargs.get('lname', '')
    email = kwargs.get('email', '')
    age = kwargs.get('age', '')
    university = kwargs.get('university', '')
    address = kwargs.get('address', '')
    
    #create new pdf
    pdf = FPDF()
    #add a pdf page
    pdf.add_page()
    #set font for pdf 
    pdf.set_font("Arial", size=12)
    #write in pdf
    pdf.cell(200, 10, txt="Form Submission Details", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Fname: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Email: {email}", ln=True)
    pdf.cell(200, 10, txt=f"Age: {age}", ln=True)
    pdf.cell(200, 10, txt=f"University: {university}", ln=True)
    pdf.cell(200, 10, txt=f"Address: {address}", ln=True)
    #create a directory to save pdf
    output_dir = os.path.join(settings.MEDIA_ROOT, 'generates_pdf')
    #if directory is not exist than create new one
    os.makedirs (output_dir, exist_ok=True)
    #save pdf file name with user first and last name
    pdf_path = os.path.join(output_dir, f"{name.replace(' ', '_')}_form.pdf")
    pdf.output(pdf_path)
    #return pdf directory path
    return f"{settings.MEDIA_URL}generates_pdf/{os.path.basename(pdf_path)}"
    