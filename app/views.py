from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from app.models import Person, Office
from django.template import Context
from django.contrib import messages

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import PersonForm

def index(request):
    return redirect('new')

def new(request):
    offices = Office.objects.order_by('name')
    context = {'offices': offices}
    return render(request, 'new.html', context)

def create(request):
    if request.method == 'POST':
        offices = Office.objects.order_by('name')
        form = PersonForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
    else:
        form = PersonForm()
    
    return render(request, 'new.html', {'form': form, 'offices': offices})


