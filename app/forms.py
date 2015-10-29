# -*- encoding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from .models import Person, Office, DocumentType
from django.utils.translation import ugettext as _
from django.utils import translation
from django.contrib import messages
import logging
from django.conf import settings

class PersonForm(forms.ModelForm):
    
    name = forms.CharField(max_length=200, required=True,
                           label=_('name'))
    surname = forms.CharField(max_length=200, required=True,
                              label=_('surname'))
    document_number = forms.CharField(max_length=10, required=True,
                                      label=_('document_number'))
    document_type = forms.ModelChoiceField(queryset=DocumentType.objects.all(),
                                           to_field_name = "id",
                                           required = True,
                                           label=_('document_type'))
    
    position = forms.CharField(max_length=200, required=False,
                               label=_('position'))
    office   = forms.ModelChoiceField(queryset=Office.objects.all(),
                                      empty_label= "(%s)" % _('specify_other'),
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
    ldap_user_password = forms.CharField( min_length=settings.MIN_LENGTH_LDAP_USER_PASSWORD, max_length=200,
                                          required=True,
                                          label=_('ldap_user_password'),
                                          widget=forms.PasswordInput())
    ldap_user_password_confirm = forms.CharField( min_length=8, max_length=200,
                                          required=True,
                                          label=_('ldap_user_password_confirm'),
                                          widget=forms.PasswordInput())
    received_application = forms.BooleanField(required=False,
                                              label=_('received_application'))
    group_id = forms.IntegerField(required=False,
                                              label=_('group_id'))

        
    class Meta:
        model = Person
        fields = ('name', 'surname', 'document_number', 'document_type', 'address', 
                  'position', 'office', 'work_phone', 'home_phone', 'other_office',
                  'group_id', 'ldap_user_password', 'ldap_user_password_confirm')

        
    def clean(self):
        ldap_user_password = self.cleaned_data.get('ldap_user_password')
        ldap_user_password_confirm = self.cleaned_data.get('ldap_user_password_confirm')
        if ldap_user_password and ldap_user_password != ldap_user_password_confirm:
            self.add_error('ldap_user_password_confirm' , _('password_dont_match') )
