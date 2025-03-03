# -*- coding: utf-8 -*-
from __future__ import unicode_literals
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
import json
from django.utils import translation
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.decorators.cache import never_cache

def set_language(request, lang='es'):
    translation.activate(lang)
    request.session[translation.LANGUAGE_SESSION_KEY] = lang
    return redirect('index')


def index(request):
    return redirect('new')


def check_ldap(request):
    existing_name_in_ldap = None
    doc_type = None
    result = False
        
    if 'ldap_user_name' in request.POST and request.POST['ldap_user_name']:
        if Person.exists_in_ldap( request.POST['ldap_user_name'] ):
            existing_name_in_ldap = request.POST['ldap_user_name']

    if 'doc_type' in request.POST and request.POST['doc_type']:
        doc_type = DocumentType.objects.get(pk=request.POST['doc_type'])
        if 'doc_num'  in request.POST and request.POST['doc_num']:
            existing_name_in_ldap = Person.ldap_uid_by_id( request.POST['doc_num'],
                                                           doc_type.name.upper() )
            
    if existing_name_in_ldap:
        result = True

    topic_list = json.dumps({'exists': result, 'uid_in_ldap': existing_name_in_ldap})
    return HttpResponse(topic_list)

def new(request):
    request.session['has_registered'] = False
    document_types = DocumentType.objects.order_by('id')
    offices = Office.objects.filter(enable=True).order_by('name')
    context = {'offices': offices, 'document_types': document_types}
    return render(request, 'new.html', context)

def send_email(message):
    recipient_list = settings.EMAIL_RECIPIENT_LIST 
    subject = 'Mollys: Solicitud de creación de cuenta para rectorado'
    from_email = settings.EMAIL_FROM 
    if subject and message and from_email and len(recipient_list)>0:
        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            logging.error(e)
    else:
        logging.error("Parámetros de envío de mail incompletos, se omite el envío.")

def create(request):
    document_types = DocumentType.objects.order_by('id')
    offices = Office.objects.order_by('name')
    context = {'offices': offices, 'document_types': document_types}
    if request.method == 'POST':

        if request.session and 'has_registered' in request.session and request.session['has_registered']:
            return redirect('new')
        
        form = PersonForm(request.POST)
        if form.is_valid():
            try:
                f = form.save()
#                f.save()
                request.session['has_registered'] = True
                
                oficina = f.office.name if (f.office and f.office.name) else ''
                tipodni = f.document_type.name if (f.document_type and f.document_type.name) else ''
                texto = """
                Se solicitó la creación de cuenta para el siguiente usuario:
                Nombre y apellido: {}, {}
                Documento: {} {}
                Email: {}
                Email alternativo: {}
                Oficina: {}

                Gestionar desde {}
                """.format(f.name, f.surname, tipodni, f.document_number, f.email, f.alternative_email,
                           oficina, settings.EMAIL_URL_ADMIN)
                send_email(texto)

                return outcome_success(request, f)
            except IntegrityError:
                logging.error('Database integrity error')
                return outcome_error(request, f)
        else:
            return render(request, 'new.html', {'form': form, 'offices': offices,
                                                'document_types': document_types})

    return render(request, 'new.html', context)


def outcome_success(request,form):
    from django.core.urlresolvers import reverse
    msg = _("outcome_success") % {'name': form.name,
                                  'surname': form.surname}

    context = {'form': form, 'msg': msg}
    return render(request, 'outcome_success.html', context)


def outcome_error(request,form):
    msg = _("outcome_error") % {'name': form.name,
                                'surname': form.surname}
    context = {'form': form, 'msg': msg}
    return render(request, 'outcome_error.html', context)


# def parag_style():
#     from  reportlab.lib.styles import ParagraphStyle
#     from reportlab.lib.enums import TA_LEFT
#     style = ParagraphStyle('test')
#     style.textColor = 'black'
#     style.borderColor = 'black'
#     style.borderWidth = 0
#     style.alignment = TA_LEFT
#     style.fontSize = 9
#     return style


# def write_header(canvas, x, y, ancho, alto):
#     from django.conf import settings
#     from reportlab.platypus import Paragraph
#     from reportlab.lib.units import cm
#     # header
#     fecha = datetime.now().strftime("%d/%m/%y %H:%M")
#     if settings.STATIC_ROOT:
#         img_path = "%s/images/logo_conduct_header.png" % settings.STATIC_ROOT
#     else:
#         img_path = "%s%simages/logo_conduct_header.png" % (settings.BASE_DIR,settings.STATIC_URL)
#     canvas.drawImage(img_path, x, y, 1.5*cm, 1.5*cm)
#     canvas.line(x,y-0.1*cm,ancho,y-0.1*cm)
#     parag = Paragraph( _("header_code"),parag_style())
#     parag.wrapOn(canvas,ancho-x,500)
#     parag.drawOn(canvas, x + 1.6*cm, y)
#     canvas.drawString(ancho-3*cm, y, fecha)


# def print_request (request, person_id):
#     from reportlab.platypus import Paragraph
#     from reportlab.lib.pagesizes import A4
#     from reportlab.lib.units import cm,inch
#     from reportlab.platypus import Paragraph
#     from reportlab.lib.styles import ParagraphStyle

#     person = Person.objects.get(id=person_id)
    
#     # configuration
#     x = 1.5*cm
#     y = 1.5*cm
#     dy = 0.5*inch
#     top = 29.7*cm - y - 1.2*y
#     right = 21*cm - x 
#     xtext = x + 3.7*cm
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="solicitud.pdf"'

#     p = canvas.Canvas(response, pagesize=A4)

#     write_header(p, x,top,right,200)
    
#     # title
#     p.drawString(xtext,top-inch,_("enabling_account").upper())

#     line = 4
#     p.drawString(x,top-line*dy, _("applicant") )
#     p.line(xtext,top-line*dy-3,right-4*cm,top-line*dy-3)
#     p.drawString(xtext,top-line*dy,person.surname_and_name())
#     line+=1
#     p.drawString(x,top-line*dy, _("doc_type") )
#     p.drawString(xtext+3*cm,top-line*dy, _("doc_number") )
#     p.line(xtext,top-line*dy-3,right-4*cm,top-line*dy-3)
#     p.drawString(xtext,top-line*dy, person.document_type.name )
#     p.drawString(xtext + 7*cm,top-line*dy, person.document_number )
#     line+=1
#     p.drawString(x,top-line*dy, _("position") )
#     p.line(xtext,top-line*dy-3,right-4*cm,top-line*dy-3)
#     p.drawString(xtext,top-line*dy,person.position)
#     line+=1
#     p.drawString(x,top-line*dy, _("work_phone"))
#     p.line(xtext,top-line*dy-3,right-4*cm,top-line*dy-3)
#     p.drawString(xtext,top-line*dy, person.work_phone or "")
#     line+=1
#     p.drawString(x,top-line*dy, _("home_phone"))
#     p.line(xtext,top-line*dy-3,right-4*cm,top-line*dy-3)
#     p.drawString(xtext,top-line*dy, person.home_phone or "")
#     line+=1
#     p.drawString(x,top-line*dy, _("address"))
#     p.line(xtext,top-line*dy-3,right-4*cm,top-line*dy-3)
#     p.drawString(xtext,top-line*dy, person.address )
#     line+=1
#     p.drawString(x,top-line*dy, _("short_office"))
#     p.line(xtext,top-line*dy-3,right-4*cm,top-line*dy-3)
#     if person.office:
#         p.drawString(xtext,top-line*dy, person.office.name)
#     else:
#         p.drawString(xtext,top-line*dy, person.other_office)
        
#     parag = Paragraph(_("intro_code"), parag_style())
#     parag.wrapOn(p,right-x,500)
#     parag.drawOn(p, x,y+0.5*inch)

#     p.showPage() # new page

#     write_header(p, x,top,right,200)
        
#     parag = Paragraph( _("conduct_code"), parag_style())
#     parag.wrapOn(p,right-x,500)
#     parag.drawOn(p, x,top-550)

#     p.drawString(x,y+3*cm, _("date"))

#     p.drawString(x+3*cm,y, _("firm"))
#     p.line(x,y+0.5*cm,250,y+0.5*cm)

#     p.drawString(x+8.4*cm,y,_('firm_responsible'))
#     p.line(280,y+0.5*cm,right,y+0.5*cm)

#     p.save()
#     return response    
