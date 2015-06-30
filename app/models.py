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

class DocumentType(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=100,null=False)
    
    class Meta:
        db_table = 'document_types'
        verbose_name_plural = 'DocumentTypes'
        
    def __unicode__(self):
        return "%s" % (self.name)

class Office(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=200,null=False)
    
    class Meta:
        db_table = 'offices'
        verbose_name_plural = 'Offices'
        
    def __unicode__(self):
        return "%s" % (self.name)

class Person(models.Model):

    def validate_existence_in_ldap(value):
        if Person.exists_in_ldap(value):
            raise ValidationError('El usuario %s ya existe.' % value)
  
    document_regex = RegexValidator(regex=r'^\d{6,10}$',
                                    message="Ingrese un valor válido")
    
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=200,null=False)
    surname = models.CharField(max_length=200,null=False)
    document_number = models.CharField(max_length=200,null=False,
                                       validators=[document_regex])
    document_type = models.ForeignKey(DocumentType, null=False, blank=False)
    position = models.CharField(max_length=200,null=True, blank=True)
    work_phone = models.CharField(max_length=200,null=True, blank=True)
    home_phone = models.CharField(max_length=200,null=True, blank=True)
    address = models.CharField(max_length=200,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    office = models.ForeignKey(Office, null=True, blank=True)
    other_office = models.CharField(max_length=200,null=True, blank=True)
    ldap_user_name = models.CharField(max_length=200,null=True, blank=True,
                                      validators=[validate_existence_in_ldap])
    received_application = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'people'
        verbose_name_plural = 'People'

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
