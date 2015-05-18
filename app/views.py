from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse
from app.models import Person

def index(request):
    return redirect('new')

def new(request):
    return render(request, 'new.html')

def create(request):
    #    if request.method == 'GET':
    #        return redirect('new')
    obj = Person(request.POST)
    print obj
    return ""


#    return render(request, 'new.html')


