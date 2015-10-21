# -*- encoding: utf-8 -*-
from django.contrib import admin
from app.models import Person, Office, Group, LdapConn
import logging
from django.forms.widgets import HiddenInput
from django.contrib import admin
from django.forms import ModelForm, PasswordInput
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
        widgets = {
            'ldap_user_password': PasswordInput(render_value=True),
        }

    def clean(self):
        if self.cleaned_data["ldap_user_name"] and not self.cleaned_data["received_application"]:
            raise forms.ValidationError( _('received_application_required') )

        if self.instance.pk and not self.cleaned_data["group_id"]:
            raise forms.ValidationError( _('required_attribute_group') )


class PersonAdmin(admin.ModelAdmin):

    form = PersonAdminForm
    list_display = ('surname', 'name', 'document_number', 'ldap_user_name',
                    'received_application')
    search_fields = ['surname', 'name', 'document_number', 'ldap_user_name',
                     'received_application']
    list_filter = (ReceivedApplicationFilter,)

    
    def change_view(self, request, object_id, form_url='', extra_context=None):

        person = Person.objects.get(id=object_id)
        enable_ldap_connection = LdapConn.enable()
        exists_in_ldap = None
        groups = None
        suggested_ldap_name = ''

        # FIXME: set form, not request.POST? 
        if 'ldap_user_password_check' in request.POST:
            request.POST['ldap_user_password'] = Person.make_secret( request.POST['ldap_user_password'] )
        if enable_ldap_connection:
            exists_in_ldap = Person.exists_in_ldap( person.ldap_user_name )
            groups = Group.all()
            suggested_ldap_name = Person.suggested_name(object_id)
        else:
            messages.warning(request, _('ldap_without_connection'))

        context = {'suggested_ldap_name': suggested_ldap_name,
                   'groups': groups,
                   'hide_save_box': (not enable_ldap_connection),
                   'exists_in_ldap': exists_in_ldap }
        
        return super(PersonAdmin, self).change_view(request, object_id,'',context)

    
admin.site.register(Person, PersonAdmin)
admin.site.register(Office)



