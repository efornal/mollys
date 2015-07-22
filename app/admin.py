from django.contrib import admin
from app.models import Person, Office
import logging


class PersonAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'document_number', 'ldap_user_name',
                    'received_application')
    search_fields = ['surname', 'name', 'document_number', 'ldap_user_name',
                     'received_application']

admin.site.register(Person, PersonAdmin)
admin.site.register(Office)


