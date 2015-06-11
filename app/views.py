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
    from reportlab.lib.units import inch
    from reportlab.lib.pagesizes import letter
    person = Person.objects.get(id=person_id)
    x = 1.8*inch
    y = 2.7*inch
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="solicitud.pdf"'
    p = canvas.Canvas(response, pagesize=letter)
    dy = 25
    top = y + 20*dy
    fecha = datetime.now().strftime("%d/%m/%y %H:%M")
    p.drawString(160,top,'FORMULARIO DE SOLICITUD DE ALTA DE USUARIO')
    p.drawString(500,top, fecha)
    p.line(490,top-3,580,top-3)

    p.drawString(30,top-2*dy,'Solicitante: ')
    p.line(120,top-2*dy-3,380,top-2*dy-3)
    p.drawString(120,top-2*dy,person.name_and_surname())

    p.drawString(30,top-3*dy,'Documento: ')
    p.line(120,top-3*dy-3,380,top-3*dy-3)
    p.drawString(120,top-3*dy,"%s %s"%(person.document_type.name,person.document_number))

    p.drawString(30,top-4*dy,'Función: ')
    p.line(120,top-4*dy-3,380,top-4*dy-3)
    p.drawString(120,top-4*dy,person.position)

    p.drawString(30,top-5*dy,'Telefonos: ')
    p.line(120,top-5*dy-3,380,top-5*dy-3)
    p.drawString(120,top-5*dy,"%s  /  %s"%(person.work_phone or "",person.home_phone or ""))

    p.drawString(30,top-6*dy,'Dirección: ')
    p.line(120,top-6*dy-3,380,top-6*dy-3)
    p.drawString(120,top-6*dy, person.address )

    p.drawString(30,top-7*dy,'Oficina: ')
    p.line(120,top-7*dy-3,380,top-7*dy-3)
    p.drawString(120,top-7*dy, person.office.name )

    p.drawString(100,top-10*dy,'Firma: ')
    p.line(160,top-10*dy-3,380,top-10*dy-3)
    p.drawString(100,top-11*dy,'Aclaración: ')
    p.line(160,top-11*dy-3,380,top-11*dy-3)

    
    p.showPage()
    p.save()
    return response    
