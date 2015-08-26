# -*- encoding: utf-8 -*-
from django.db import models
from datetime import datetime
from django.core.validators import RegexValidator
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import logging
import ldap
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.translation import ugettext as _
import unicodedata

def validate_group_existence_in_ldap(value):
    if not (value > 0):
        raise ValidationError("The group identified as '%s' does not exist" % value)


class LdapConn():

    @classmethod
    def new(cls):
        try:
            connection = ldap.initialize( settings.LDAP_SERVER )
            connection.simple_bind_s( "cn=%s,%s" % ( settings.LDAP_USER_NAME, settings.LDAP_DN ),
                                      settings.LDAP_USER_PASS )
            return connection

        except ldap.LDAPError:
            logging.error("Could not connect to the Ldap server: '%s'" % settings.LDAP_SERVER )
            raise
        except e:
            logging.error(e)
            raise

    @classmethod
    def enable(cls):
        try:
            connection = ldap.initialize( settings.LDAP_SERVER )
            connection.simple_bind_s( "cn=%s,%s" % ( settings.LDAP_USER_NAME, settings.LDAP_DN ),
                                      settings.LDAP_USER_PASS )
            return connection
        except ldap.LDAPError, e:
            return None
        
    @classmethod
    def parseattr (cls, s):
        return s.encode("utf8","ignore")
    
    
class DocumentType(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=100,null=False)
    
    class Meta:
        db_table = 'document_types'
        verbose_name = _('DocumentType')
        verbose_name_plural = _('DocumentTypes')
        
    def __unicode__(self):
        return self.name

    
class Office(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=200, null=False, verbose_name=_('name'))
    
    class Meta:
        db_table = 'offices'
        verbose_name = _('office')
        verbose_name_plural = _('offices')

    def __unicode__(self):
        return self.name

    
class Group(models.Model):
    group_id = models.IntegerField()
    name = models.CharField(max_length=200)
    
    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')
        managed = False
        
        
    def __unicode__(self):
        return self.name

    @classmethod
    def cn_group_by_gid(cls, gid):
        ldap_condition = "(gidNumber=%s)" % gid
        cn_found = None

        r = LdapConn.new().search_s("ou=%s,%s" %(settings.LDAP_GROUP, settings.LDAP_DN),
                                    ldap.SCOPE_SUBTREE,
                                    ldap_condition,
                                    ['cn'])
        for dn,entry in r:
            if 'cn' in entry and entry['cn'][0]:
                cn_found = entry['cn'][0]

        return cn_found
    
    @classmethod
    def all(cls):
        ldap_condition = "(&(cn=*)(%s>=%s))"  % (settings.LDAP_GROUP_FIELDS[0],
                                                 settings.LDAP_GROUP_MIN_VALUE)
        rows = []

        r = LdapConn.new().search_s( "ou=%s,%s" %(settings.LDAP_GROUP, settings.LDAP_DN),
                                     ldap.SCOPE_SUBTREE,
                                     ldap_condition,
                                     settings.LDAP_GROUP_FIELDS )
        for dn,entry in r:
            row = {}
            if settings.LDAP_GROUP_FIELDS[0] in entry \
               and settings.LDAP_GROUP_FIELDS[1] in entry:
                row[settings.LDAP_GROUP_FIELDS[0]] = int(entry[settings.LDAP_GROUP_FIELDS[0]][0])
                row[settings.LDAP_GROUP_FIELDS[1]] = entry[settings.LDAP_GROUP_FIELDS[1]][0]
                rows.append(row)
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
                                      verbose_name=_('ldap_user_name'))#,
                                      #validators=[validate_existence_in_ldap])
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
        return self.name

    def name_and_surname(self):
        return "%s, %s" % (self.name, self.surname)

    def surname_and_name(self):
        return "%s, %s" % (self.surname, self.name)

    @classmethod
    def next_ldap_uid(cls):
        ldap_condition = "(uidNumber=*)"
        next_value = 0
        ldap_dn ="ou=%s,%s" %(settings.LDAP_PEOPLE, settings.LDAP_DN)

        r = LdapConn.new().search_s(ldap_dn,ldap.SCOPE_SUBTREE,
                                    ldap_condition,
                                    ['uidNumber'])

        for dn,entry in r:
            if entry['uidNumber'][0] and int(entry['uidNumber'][0]) > next_value:
                next_value = int(entry['uidNumber'][0])
                if next_value > 0:
                    next_value += 1

        return next_value
        

    @classmethod
    def exists_in_ldap(cls,uid):
        ldap_condition = "(uid=%s)" % uid

        r = LdapConn.new().search_s("ou=%s,%s" %(settings.LDAP_PEOPLE, settings.LDAP_DN),
                                    ldap.SCOPE_SUBTREE,
                                    ldap_condition,
                                    settings.LDAP_PEOPLE_FIELDS)
        for dn,entry in r:
            if entry['uid'][0] == uid:
                return True
        return False

    @classmethod
    def compose_suggested_name( cls, surname, name ):
        return Person.strip_accents( "%s%s" % ( name.strip()[0].lower(),
                                                surname.lower().strip().partition(" ")[0] ) )

    @classmethod
    def compose_extended_suggested_name( cls, surname, name ):
        names = ""
        for word in name.lower().strip().split(" "):
            if len(word) > 1: names += word[0] 
        return Person.strip_accents( "%s%s" % ( names,
                                                surname.lower().strip().partition(" ")[0] ) )

    @classmethod
    def strip_accents(cls,s):
        if not isinstance(s, unicode):
            text = unicodedata.normalize('NFKD', unicode(s, 'utf8'))
            return u"".join([c for c in text if not unicodedata.combining(c)])
        else:
            return ''.join(c for c in unicodedata.normalize('NFD', s)
                           if unicodedata.category(c) != 'Mn')

    @classmethod
    def suggested_name( cls, object_id ):
        person = Person.objects.get(id=object_id)
        first_try = Person.compose_suggested_name(person.surname, person.name)

        if  Person.exists_in_ldap(first_try):
            return Person.compose_extended_suggested_name(person.surname, person.name)
        else:
            return first_try

@receiver(post_save, sender=Person)
def update_ldap_user(sender, instance, *args, **kwargs):

    ldap_user_name = str(instance.ldap_user_name) if instance.ldap_user_name else None

    if ldap_user_name is None:
        logging.info("An LDAP user was not given. It is not updated!")
    elif ldap_user_name and Person.exists_in_ldap(ldap_user_name):
        logging.info("User %s already exists in Ldap. It is not updated!" % ldap_user_name)
    elif ldap_user_name:

        new_uid_number = Person.next_ldap_uid()
        cn_group = Group.cn_group_by_gid(instance.group_id)

        udn = "uid=%s,ou=%s,%s" % ( ldap_user_name,
                                    settings.LDAP_PEOPLE,
                                    settings.LDAP_DN )
        gdn = "cn=%s,ou=%s,%s" % ( cn_group,
                                   settings.LDAP_GROUP,
                                   settings.LDAP_DN )

        cnuser = LdapConn.parseattr( "%s %s" % (instance.name, instance.surname) )
        snuser = LdapConn.parseattr( "%s" % instance.surname )

        new_user = [
            ('objectclass', settings.LDAP_PEOPLE_OBJECTCLASSES),
            ('cn', [cnuser]),
            ('sn', [snuser]),
            ('givenName', [ LdapConn.parseattr(instance.name)] ),
            ('paisdoc', [settings.LDAP_PEOPLE_PAISDOC] ),
            ('tipodoc', [str(instance.document_type)] ),
            ('numdoc', [str(instance.document_number)] ),
            ('uidNumber', [str(new_uid_number)] ),
            ('homedirectory', [str('%s%s' % ( settings.LDAP_PEOPLE_HOMEDIRECTORY_PREFIX,
                                              ldap_user_name))]),
            ('gidNumber', [str(instance.group_id)] ),
            ('ou', [str(settings.LDAP_PEOPLE)]),
        ]
            
        update_group = [( ldap.MOD_ADD, 'memberUid', ldap_user_name )]
        
        logging.info("Creating user in Ldap: %s " % new_user )
        LdapConn.new().add_s(udn, new_user)

        logging.info("Adding new member in ldap: %s " % update_group )
        LdapConn.new().modify(gdn, update_group)
