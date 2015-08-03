from django.contrib import admin
from app.models import Person, Office
import logging


class PersonAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'document_number', 'ldap_user_name',
                    'received_application')
    search_fields = ['surname', 'name', 'document_number', 'ldap_user_name',
                     'received_application']

    def change_view(self, request, object_id, form_url='', extra_context=None):
        #self.inlines = (ItemChangeInline, )
        Person.suggested_name(object_id)
        context = {'suggested_ldap_name': Person.suggested_name(object_id) }
        return super(PersonAdmin, self).change_view(request, object_id,'',context)
    
admin.site.register(Person, PersonAdmin)
admin.site.register(Office)


