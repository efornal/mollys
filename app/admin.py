# -*- encoding: utf-8 -*-
from django.contrib import admin
from app.models import Person, Office, Group
import logging
from django.forms.widgets import HiddenInput
from django.contrib import admin
from django import forms

 
class PersonAdminForm(forms.ModelForm):
    
    class Meta:
        model = Person
        fields = '__all__'
        
    def clean(self):
        if self.cleaned_data["ldap_user_name"] and not self.cleaned_data["received_application"]:
            raise forms.ValidationError( "No es posible asignar un usuario ldap " \
                                         "sin confirmar la 'solicitud recibida'" )

        if self.instance.pk and not self.cleaned_data["group_id"]:
            raise forms.ValidationError( "El atributo 'Grupo' es requerido")                 
    
class PersonAdmin(admin.ModelAdmin):
    form = PersonAdminForm
    list_display = ('surname', 'name', 'document_number', 'ldap_user_name',
                    'received_application')
    search_fields = ['surname', 'name', 'document_number', 'ldap_user_name',
                     'received_application']
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        person = Person.objects.get(id=object_id)
        exists_in_ldap = Person.exists_in_ldap( person.ldap_user_name )
        groups = Group.all()
        context = {'suggested_ldap_name': Person.suggested_name(object_id),
                   'groups': groups,
                   'exists_in_ldap': exists_in_ldap }
        return super(PersonAdmin, self).change_view(request, object_id,'',context)

    
admin.site.register(Person, PersonAdmin)
admin.site.register(Office)



