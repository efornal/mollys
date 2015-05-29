# -*- encoding: utf-8 -*-
from django.db import models
from datetime import datetime

    
class Office(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=200,null=False)
    
    class Meta:
        db_table = 'offices'
        verbose_name_plural = 'Offices'
        
    def __unicode__(self):
        return "%s" % (self.name)

class Person(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=200,null=False)
    surname = models.CharField(max_length=200,null=False)
    document_number = models.CharField(max_length=200,null=False)
    document_type = models.IntegerField(null=False)
    position = models.CharField(max_length=200,null=True, blank=True)
    work_phone = models.CharField(max_length=200,null=True)
    home_phone = models.CharField(max_length=200,null=True)
    address = models.CharField(max_length=200,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    office = models.ForeignKey(Office, null=True, blank=True)
    
    class Meta:
        db_table = 'people'
        verbose_name_plural = 'People'

    def __unicode__(self):
        return "%s" % (self.name)

