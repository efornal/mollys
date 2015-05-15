from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return redirect('new')

def new(request):
    return render(request, 'new.html')


