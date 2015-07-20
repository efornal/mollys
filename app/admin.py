from django.contrib import admin
from app.models import Person, Office
import logging


class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'document_number')
    search_fields = ['name', 'surname', 'document_number']

admin.site.register(Person, PersonAdmin)
admin.site.register(Office)


