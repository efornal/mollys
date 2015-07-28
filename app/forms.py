# -*- encoding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from .models import Person, Office, DocumentType
from django.utils.translation import ugettext as _
from django.utils import translation

class PersonForm(forms.ModelForm):
    name = forms.CharField(max_length=200, required=True)

    surname = forms.CharField(max_length=200, required=True)

    document_number = forms.CharField(max_length=10, required=True)

    document_type = forms.ModelChoiceField(queryset=DocumentType.objects.all(),
                                           to_field_name = "id",
                                           required = True)
    
    position = forms.CharField(max_length=200, required=False)
    office   = forms.ModelChoiceField(queryset=Office.objects.all(),
                                      empty_label="(Especificar Otra)",
                                      to_field_name= "id",
                                      required=False)
    work_phone = forms.CharField(max_length=200, required=False)
    home_phone = forms.CharField(max_length=200, required=False)
    address = forms.CharField(max_length=200, required=False)
    created_at = forms.DateTimeField(required=False)
    updated_at = forms.DateTimeField(required=False)
    other_office = forms.CharField(max_length=200, required=False)
    ldap_user_name = forms.CharField(max_length=200,required=False)
    received_application = forms.BooleanField(required=False)

    class Meta:
        model = Person
        fields = ('name', 'surname', 'document_number', 'document_type', 'address',
                  'position', 'office', 'work_phone', 'home_phone', 'other_office')

