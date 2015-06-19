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


def print_request (request, person_id):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch, cm
    person = Person.objects.get(id=person_id)
    x = 1*inch
    y = 2.7*inch
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="solicitud.pdf"'
    p = canvas.Canvas(response, pagesize=letter)
    dy = 0.5*inch
    top = y + 6.5*inch
    right = x + 7*inch
    fecha = datetime.now().strftime("%d/%m/%y %H:%M")
    xtext = x + 1.2*inch
    
    # header
    p.drawImage('static/images/unl.png', x, top, inch, inch)
    p.line(x,top-3,right,top-3)
    p.drawString(xtext,top+0.7*inch,'Dirección de Informatización y Planificación Tecnológica')
    p.drawString(xtext,top+0.4*inch,'Rectorado')
    p.drawString(xtext,top+0.1*inch,'Universidad Nacional del Litoral')
    p.drawString(right-1.1*inch,top, fecha)
    
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

    line+=1
    p.drawString(x,top-line*dy,"La DIPT (Dirección de Informatización y Planificación Tecnológica) habilita cuentas en sus servidores")
    line+=1
    p.drawString(x,top-line*dy, "y/o permitirá la habilitación de cuentas ...")

    p.showPage() # new page
    
    line+=2
    p.drawString(xtext,top-line*dy,'Firma: ')
    p.line(xtext+60,top-line*dy-3,380,top-line*dy-3)
    line+=1
    p.drawString(xtext,top-line*dy,'Aclaración: ')
    p.line(xtext+60,top-line*dy-3,380,top-line*dy-3)

    p.save()
    return response    
