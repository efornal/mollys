# -*- encoding: utf-8 -*-
from django.db import models
from datetime import datetime
from django.core.validators import RegexValidator
from django.db.models.signals import pre_save
from django.dispatch import receiver
import logging
import ldap
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.translation import ugettext as _

def validate_group_existence_in_ldap(value):
    if not (value > 0):
        raise ValidationError('El grupo identificado con %s no existe.' % value)

class DocumentType(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=100,null=False)
    
    class Meta:
        db_table = 'document_types'
        verbose_name = _('DocumentType')
        verbose_name_plural = _('DocumentTypes')
        
    def __unicode__(self):
        return "%s" % (self.name)

class Office(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=200, null=False, verbose_name=_('name'))
    
    class Meta:
        db_table = 'offices'
        verbose_name = _('office')
        verbose_name_plural = _('offices')

    def __unicode__(self):
        return "%s" % (self.name)

class Group(models.Model):
    group_id = models.IntegerField()
    name = models.CharField(max_length=200)
    
    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')
        managed = False
        
        
    def __unicode__(self):
        return ""
    
    @classmethod
    def all(cls):
        ldap_condition = "(cn=*)"
        rows = []
        try:
            l = ldap.initialize( settings.LDAP_SERVER )
            r = l.search_s( "%s,%s" %(settings.LDAP_GROUP, settings.LDAP_DN),
                            ldap.SCOPE_SUBTREE, ldap_condition, settings.LDAP_GROUP_FIELDS )
            for dn,entry in r:
                row = {}
                if settings.LDAP_GROUP_FIELDS[0] in entry and settings.LDAP_GROUP_FIELDS[1] in entry:
                    row[settings.LDAP_GROUP_FIELDS[0]] = int(entry[settings.LDAP_GROUP_FIELDS[0]][0])
                    row[settings.LDAP_GROUP_FIELDS[1]] = entry[settings.LDAP_GROUP_FIELDS[1]][0]
                    rows.append(row)
        except ldap.LDAPError, e:
            logging.error(e)
        return rows
    
    
class Person(models.Model):

    document_regex = RegexValidator(regex=r'^\d{6,10}$',
                                    message=_('invalid_value'))
    
    id = models.AutoField(primary_key=True, null=False)
    name = models.CharField(max_length=200, null=False,
                            verbose_name=_('names'))
    surname = models.CharField(max_length=200,null=False,
                               verbose_name=_('surnames'))
    document_number = models.CharField(max_length=200,null=False,
                                       validators=[document_regex],
                                       verbose_name=_('document_number'))
    document_type = models.ForeignKey(DocumentType, null=False, blank=False,
                                      verbose_name=_('document_type'))
    position = models.CharField(max_length=200,null=True, blank=True,
                                verbose_name=_('position'))
    work_phone = models.CharField(max_length=200,null=True, blank=True,
                                  verbose_name=_('work_phone'))
    home_phone = models.CharField(max_length=200,null=True, blank=True,
                                  verbose_name=_('home_phone'))
    address = models.CharField(max_length=200,null=True, blank=True,
                               verbose_name=_('address'))
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('created_at'))
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_('updated_at'))
    office = models.ForeignKey(Office, null=True, blank=True,
                               verbose_name=_('office'))
    other_office = models.CharField(max_length=200,null=True, blank=True,
                                    verbose_name=_('other_office'))
    ldap_user_name = models.CharField(max_length=200,null=True, blank=True,
                                      verbose_name=_('ldap_user_name'))
 #                                     validators=[validate_existence_in_ldap])
    received_application = models.BooleanField(default=False,
                                               verbose_name=_('received_application'))
    group_id = models.IntegerField(null=True, blank=True, verbose_name=_('group_id'))

    # models.IntegerField(null=True, blank=True,
    #                                verbose_name=_('group_id'),
    #                                validators=[validate_group_existence_in_ldap])
    
    class Meta:
        db_table = 'people'
        verbose_name = _('person')
        verbose_name_plural = _('people')

    def __unicode__(self):
        return "%s" % (self.name)

    def name_and_surname(self):
        return "%s, %s" % (self.name, self.surname)

    def surname_and_name(self):
        return "%s, %s" % (self.surname, self.name)


    @classmethod
    def exists_in_ldap(cls,uid):
        ldap_condition = "(uid=%s)" % uid
        try:
            l = ldap.initialize( settings.LDAP_SERVER )
            r = l.search_s("%s,%s" %(settings.LDAP_PEOPLE, settings.LDAP_DN),
                           ldap.SCOPE_SUBTREE, ldap_condition, settings.LDAP_PEOPLE_FIELDS)
            
            for dn,entry in r:
                if entry['uid'][0] == uid:
                    return True

        except ldap.LDAPError, e:
            logging.error(e)
        return False

    @classmethod
    def compose_suggested_name( cls, surname, name ):
        return "%s%s" % ( name[0].lower(), surname.lower().partition(" ")[0] )

    @classmethod
    def compose_extended_suggested_name( cls, surname, name ):
        words = ""
        for word in name.lower().split(" "):
            words += word[0]
        return "%s%s" % ( words, surname.lower().partition(" ")[0] )

    @classmethod
    def suggested_name( cls, object_id ):
        person = Person.objects.get(id=object_id)
        first_try = Person.compose_suggested_name(person.surname, person.name)

        if  Person.exists_in_ldap(first_try):
            return Person.compose_extended_suggested_name(person.surname, person.name)
        else:
            return first_try
