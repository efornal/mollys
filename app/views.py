# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from app.models import Person, Office
from django.template import Context
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import PersonForm
import logging

def index(request):
    return redirect('new')

def new(request):
    offices = Office.objects.order_by('name')
    context = {'offices': offices}
    return render(request, 'new.html', context)

def create(request):
    offices = Office.objects.order_by('name')
    
    if request.method == 'POST':
        office_id = request.POST.get('office') or None
        office  = Office.objects.get(id=office_id)
        form = PersonForm(request.POST)
        form.office = office
        
        if form.is_valid():
            try:
                f = form.save(commit=False)
                f.save()
                message = 'La solicitud se realizó con éxito.'
            except IntegrityError:
                message = 'La solicitud no pudo realizarse.'
                logging.error('Error de integridad en la base de datos.')

            request.session['message'] = message
            return redirect('outcome')
        else:
            return render(request, 'new.html', {'form': form, 'offices': offices})

    return render(request, 'new.html', {'offices': offices})

def outcome(request):
    context = {'message': request.session.get('message')}
    return render(request, 'outcome.html', context)

