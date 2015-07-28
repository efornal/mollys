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

class Person(models.Model):

#    def validate_existence_in_ldap(value):
#        if Person.exists_in_ldap(value):
#            raise ValidationError('El usuario %s ya existe.' % value)
  
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
    
    class Meta:
        db_table = 'people'
        verbose_name = _('person')
        verbose_name_plural = _('people')

    def __unicode__(self):
        return "%s" % (self.name)

    def name_and_surname(self):
        return "%s, %s" % (self.name, self.surname)

    @classmethod
    def exists_in_ldap(cls,uid):
        ldap_condition = "(uid=%s)" % uid
        logging.info("LDAP condition: %s" % ldap_condition)
        try:
            l = ldap.initialize( settings.LDAP_SERVER )
            r = l.search_s(settings.LDAP_DN, ldap.SCOPE_SUBTREE, ldap_condition)
            
            for dn,entry in r:
                logging.info("LDAP user search: %s=%s?" % (entry['uid'][0],uid))
                if entry['uid'][0] == uid:
                    logging.info("LDAP User: %s, found!: " % entry['uid'][0])
                    return True
        except ldap.LDAPError, e:
            logging.error(e)
        return False
