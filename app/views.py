# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from app.models import Person, Office, DocumentType
from django.template import Context
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import PersonForm
from datetime import datetime
import logging
from reportlab.pdfgen import canvas
from django.conf import settings
from django.utils.translation import ugettext as _

def index(request):
    return redirect('new')

def new(request):
    document_types = DocumentType.objects.order_by('id')
    offices = Office.objects.order_by('name')
    context = {'offices': offices, 'document_types': document_types}
    return render(request, 'new.html', context)

def create(request):
    document_types = DocumentType.objects.order_by('id')
    offices = Office.objects.order_by('name')
    context = {'offices': offices, 'document_types': document_types}
    if request.method == 'POST':
        logging.info("POST (New People): %s" % request.POST)
        
        form = PersonForm(request.POST)
        if form.is_valid():
            try:
                f = form.save(commit=False)
                f.save()
                return outcome_success(request, f)
            except IntegrityError:
                logging.error('Error de integridad en la base de datos.')
                return outcome_error(request, f)
        else:
            return render(request, 'new.html', {'form': form, 'offices': offices,
                                                'document_types': document_types})

    return render(request, 'new.html', context)


def outcome_success(request,form):
    logging.error("Form: %s" % form )
    context = {'form': form}
    return render(request, 'outcome_success.html', context)


def outcome_error(request,form):
    logging.error("Form: %s" % form )
    context = {'form': form}
    return render(request, 'outcome_error.html', context)


def parag_style():
    from  reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_LEFT
    style = ParagraphStyle('test')
    style.textColor = 'black'
    style.borderColor = 'black'
    style.borderWidth = 0
    style.alignment = TA_LEFT
    style.fontSize = 9
    return style
    
def write_header(canvas, x, y, ancho, alto):
    from reportlab.platypus import Paragraph
    from reportlab.lib.units import cm
    # header
    fecha = datetime.now().strftime("%d/%m/%y %H:%M")
    canvas.drawImage('static/images/logo_conduct_header.png', x, y, 1.5*cm, 1.5*cm)
    canvas.line(x,y-0.1*cm,ancho,y-0.1*cm)
    parag = Paragraph(load_file(settings.CODE_FILES['header']),parag_style())
    parag.wrapOn(canvas,ancho-x,500)
    parag.drawOn(canvas, x + 1.6*cm, y)
    canvas.drawString(ancho-3*cm, y, fecha)

def load_file(filename):
    f = open(filename, 'r')
    content = f.read()
    f.close()
    return content

def print_request (request, person_id):
    from reportlab.platypus import Paragraph
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm,inch
    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import ParagraphStyle

    person = Person.objects.get(id=person_id)
    
    # configuration
    x = 1.5*cm
    y = 1.5*cm
    dy = 0.5*inch
    top = 29.7*cm - y - 1.2*y
    right = 21*cm - x 
    xtext = x + 1.2*inch
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="solicitud.pdf"'
    p = canvas.Canvas(response, pagesize=A4)


    write_header(p, x,top,right,200)
    
    # title
    p.drawString(xtext,top-inch,'SOLICITUD DE HABILITACIÓN DE CUENTA')

    line = 4
    p.drawString(x,top-line*dy,'Solicitante: ')
    p.line(xtext,top-line*dy-3,380,top-line*dy-3)
    p.drawString(xtext,top-line*dy,person.name_and_surname())
    line+=1
    p.drawString(x,top-line*dy,'Documento: ')
    p.line(xtext,top-line*dy-3,380,top-line*dy-3)
    p.drawString(xtext,top-line*dy,"%s %s"%(person.document_type.name,person.document_number))
    line+=1
    p.drawString(x,top-line*dy,'Función: ')
    p.line(xtext,top-line*dy-3,380,top-line*dy-3)
    p.drawString(xtext,top-line*dy,person.position)
    line+=1
    p.drawString(x,top-line*dy,'Telefonos: ')
    p.line(xtext,top-line*dy-3,380,top-line*dy-3)
    p.drawString(xtext,top-line*dy,"%s  /  %s"%(person.work_phone or "",person.home_phone or ""))
    line+=1
    p.drawString(x,top-line*dy,'Dirección: ')
    p.line(xtext,top-line*dy-3,380,top-line*dy-3)
    p.drawString(xtext,top-line*dy, person.address )
    line+=1
    p.drawString(x,top-line*dy,'Oficina: ')
    p.line(xtext,top-line*dy-3,380,top-line*dy-3)
    p.drawString(xtext,top-line*dy, person.office.name )

    
    parag = Paragraph(load_file(settings.CODE_FILES['intro']), parag_style())
    parag.wrapOn(p,right-x,500)
    parag.drawOn(p, x,y+0.5*inch)

    p.showPage() # new page

    write_header(p, x,top,right,200)
        
    parag = Paragraph(load_file(settings.CODE_FILES['conduct']), parag_style())
    parag.wrapOn(p,right-x,500)
    parag.drawOn(p, x,top-550)

    p.drawString(x,y+3*cm,'Santa Fe, ...... de ............. de 20....')

    p.drawString(xtext-5,y,'Firma ')
    p.line(x,y+0.5*cm,260,y+0.5*cm)

    p.drawString(x+8.2*cm,y,'Firma y aclaración del responsable del área/sector ')
    p.line(270,y+0.5*cm,right,y+0.5*cm)

    p.save()
    return response    
