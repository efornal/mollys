# -*- encoding: utf-8 -*-
from django.contrib import admin
from app.models import Person, Office, Group, LdapConn, DocumentType
import logging
from django.forms.widgets import HiddenInput
from django.contrib import admin
from django.forms import ModelForm, PasswordInput
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.conf import settings
import ldap
from django.core.exceptions import ValidationError


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
            self.add_error('received_application',_('received_application_required') )

        if self.instance.pk and not self.cleaned_data["group_id"]:
            self.add_error('group_id',_('required_attribute_group') )
            raise ValidationError(_('required_attribute_group'))

        if len(self.cleaned_data['ldap_user_password']) < settings.MIN_LENGTH_LDAP_USER_PASSWORD:
            raise ValidationError(_('ldap_user_password_too_short'))
        existing_name_in_ldap = Person.ldap_uid_by_id( self.cleaned_data['document_number'],
                                                       self.cleaned_data['document_type'] )

        if self.cleaned_data["ldap_user_name"]:
            existing_name_in_ldap = Person.ldap_uid_by_id( self.cleaned_data['document_number'],
                                                           self.cleaned_data['document_type'] )
            if existing_name_in_ldap and (existing_name_in_ldap is self.cleaned_data["ldap_user_name"]):
                logging.info("User has already exists in Ldap with uid '%s'. it was not updated!" \
                             % existing_name_in_ldap)
                self.add_error('document_number',
                               "Ya existe en Ldap un usuario con este Documento cuyo uid es '%s'" \
                               % existing_name_in_ldap)


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


    def save_model(self, request, obj, form, change):
        ldap_user_name = str(obj.ldap_user_name) if obj.ldap_user_name else None
        udn = Person.ldap_udn_for( ldap_user_name )
        
        try:
            if (not ldap_user_name) or (ldap_user_name is None):
                message = "An LDAP user was not given. It is not updated!"
                logging.warning(message)
                raise ValidationError(message)
    
            if Person.exists_in_ldap(ldap_user_name): # actualizar
                ldap_person = Person.get_from_ldap(ldap_user_name)

                # update data
                ldap_person.update_ldap_data_from(obj)
        
                # update password only for superuser
                if str(ldap_person.ldap_user_password) != str(obj.ldap_user_password) \
                   and request.POST.has_key('ldap_user_password_check'):
                    if request.user.is_superuser:
                        logging.warning("User '%s' already exists in Ldap. changing password.." % ldap_user_name)
                        Person.update_ldap_user_password ( ldap_user_name, str(obj.ldap_user_password) )
                    else:
                        raise ValidationError('The user does not have permission to change the password')
                    
                # update group
                if str(ldap_person.group_id) != str(obj.group_id):
                    if request.user.is_superuser:
                        logging.warning("User '%s' already exists in Ldap. Changing group '%s' by '%s'.." % \
                                     (ldap_user_name,ldap_person.group_id, obj.group_id ) )
                        Group.add_member_to(ldap_user_name, {'group_id': str(obj.group_id)})
                        Group.remove_member_of(ldap_user_name, ldap_person.group_id)
                        ldap_person.update_ldap_gidgroup( str(obj.group_id) )
                    else:
                        raise ValidationError('The user does not have permission to change the group')

            else: # crear nuevo
                new_uid_number = Person.next_ldap_uidNumber()
                if not (new_uid_number > 0):
                    logging.error( "The following 'ldap user uid' could not be determined. " \
                                   "The value obtained was %s" % str(new_uid_number))
                    raise ValidationError("The 'ldap user uid' could not be determined.'")

                if Person.exist_ldap_uidNumber(new_uid_number):
                    logging.error("The ldap user uidNumber '%s' already exist!." % str(new_uid_number))
                    new_uid_number = 0
                    raise ValidationError("The ldap user uidNumber already exist!")

                # Create new ldapp user
                cnuser = LdapConn.parseattr( "%s %s" % (obj.name, obj.surname) )
                snuser = LdapConn.parseattr( "%s" % obj.surname )
                new_user = [
                    ('objectclass', settings.LDAP_PEOPLE_OBJECTCLASSES),
                    ('cn', [cnuser]),
                    ('sn', [snuser]),
                    ('givenName', [ LdapConn.parseattr(obj.name)] ),
                    ('paisdoc', [settings.LDAP_PEOPLE_PAISDOC] ),
                    ('tipodoc', [str(obj.document_type)] ),
                    ('numdoc', [str(obj.document_number)] ),
                    ('uidNumber', [str(new_uid_number)] ),
                    ('userPassword', [str(obj.ldap_user_password)] ),
                    ('telephoneNumber', [str(obj.work_phone)] ),
                    ('physicalDeliveryOfficeName', [str(obj.office_name())] ),
                    ('homedirectory', [str('%s%s' % ( settings.LDAP_PEOPLE_HOMEDIRECTORY_PREFIX,
                                                      ldap_user_name))]),
                    ('gidNumber', [str(obj.group_id)] ),
                    ('loginShell', [str(settings.LDAP_PEOPLE_LOGIN_SHELL)]),]

                Person.create_ldap_user( ldap_user_name, new_user )

                # Update ldap groups
                cn_group = Group.cn_group_by_gid(obj.group_id)
                cn_groups = ['%s' % str(cn_group)]
                if settings.LDAP_DEFAULT_GROUPS:
                    cn_groups += settings.LDAP_DEFAULT_GROUPS

                Group.add_member_in_groups( ldap_user_name, cn_groups )

            obj.save()
            
        except ValidationError as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request,"Error updating user. %s" % e[0])

        
admin.site.register(Person, PersonAdmin)
admin.site.register(Office)



