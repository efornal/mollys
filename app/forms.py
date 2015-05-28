# -*- encoding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from .models import Person, Office

class PersonForm(forms.ModelForm):
    name = forms.CharField(max_length=200, required=True,
        error_messages = {'required': 'Es un atributo requerido.'},
        label = 'Nombre')

    surname = forms.CharField(max_length=200, required=True,
        error_messages = {'required': 'Es un atributo requerido.'},
        label = 'Apellido')

    document_number = forms.CharField(max_length=10, required=True,
        error_messages = {'required': 'Es un atributo requerido.',
                          'invalid': 'Ingrese un valor válido'},
        label = 'Nro. documento')

    document_type = forms.IntegerField(required=True,
        error_messages = {'required': 'Es un atributo requerido.',
                          'invalid': 'Ingrese un valor válido'},
        label = 'Tipo documento')

    position = forms.CharField(max_length=200, required=False)
    office   = Office
    work_phone = forms.CharField(max_length=200, required=False)
    home_phone = forms.CharField(max_length=200, required=False)
    address = forms.CharField(max_length=200, required=False)
    created_at = forms.DateTimeField(required=False)
    updated_at = forms.DateTimeField(required=False)

    class Meta:
        model = Person
        fields = ('name', 'surname', 'document_number', 'document_type', 'address',
                  'position', 'office', 'work_phone', 'home_phone')

