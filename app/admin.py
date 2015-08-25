# -*- encoding: utf-8 -*-
from django.contrib import admin
from app.models import Person, Office, Group
import logging
from django.forms.widgets import HiddenInput
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
import ldap

class ReceivedApplicationFilter(admin.SimpleListFilter):
    title = _('received_application')

    parameter_name = 'received_application'

    def lookups(self, request, model_admin):
        return (
            (None, _('No')),
            ('yes', _('Yes')),
            ('all', _('All')),
        )

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(received_application=True)    
        elif self.value() == None:
            return queryset.filter(received_application=False)


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
    list_filter = (ReceivedApplicationFilter,)
    
    def change_view(self, request, object_id, form_url='', extra_context=None):

        person = Person.objects.get(id=object_id)
        exists_in_ldap = None
        groups = None
        suggested_ldap_name = ''
        
        try:
            exists_in_ldap = Person.exists_in_ldap( person.ldap_user_name )
            groups = Group.all()
            suggested_ldap_name = Person.suggested_name(object_id)
        except ldap.LDAPError, e:
            logging.error(e)
            messages.error(request, 'No se pudo establecer la conexión con el servidor Ldap')
    
        context = {'suggested_ldap_name': suggested_ldap_name,
                   'groups': groups,
                   'exists_in_ldap': exists_in_ldap }
        
        return super(PersonAdmin, self).change_view(request, object_id,'',context)

    
admin.site.register(Person, PersonAdmin)
admin.site.register(Office)



