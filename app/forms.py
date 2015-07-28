# -*- encoding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from .models import Person, Office, DocumentType
from django.utils.translation import ugettext as _
from django.utils import translation

class PersonForm(forms.ModelForm):
    name = forms.CharField(max_length=200, required=True,
                           label=_('names'))
    surname = forms.CharField(max_length=200, required=True,
                              label=_('surnames'))
    document_number = forms.CharField(max_length=10, required=True,
                                      label=_('document_number'))
    document_type = forms.ModelChoiceField(queryset=DocumentType.objects.all(),
                                           to_field_name = "id",
                                           required = True,
                                           label=_('document_type'))
    
    position = forms.CharField(max_length=200, required=False,
                               label=_('position'))
    office   = forms.ModelChoiceField(queryset=Office.objects.all(),
                                      empty_label="(Especificar Otra)",
                                      to_field_name= "id",
                                      required=False,
                                      label=_('office'))
    work_phone = forms.CharField(max_length=200, required=False,
                                 label=_('work_phone'))
    home_phone = forms.CharField(max_length=200, required=False,
                                 label=_('home_phone'))
    address = forms.CharField(max_length=200, required=False,
                              label=_('address'))
    created_at = forms.DateTimeField(required=False,
                                     label=_('created_at'))
    updated_at = forms.DateTimeField(required=False,
                                     label=_('updated_at'))
    other_office = forms.CharField(max_length=200, required=False,
                                   label=_('other_office'))
    ldap_user_name = forms.CharField(max_length=200,required=False,
                                     label=_('ldap_user_name'))
    received_application = forms.BooleanField(required=False,
                                              label=_('received_application'))

    class Meta:
        model = Person
        fields = ('name', 'surname', 'document_number', 'document_type', 'address',
                  'position', 'office', 'work_phone', 'home_phone', 'other_office')

