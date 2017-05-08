# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from django.core.validators import RegexValidator
from django.db.models.signals import pre_save, post_save
from django.contrib.auth import logout
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
import logging
import ldap
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.translation import ugettext as _
import unicodedata
import hashlib
import os
import re


    
def validate_ldap_user_password(value):
    if not Person.ldap_password_valid(value):
        raise ValidationError(_('ldap_user_password_invalid'))

    
def validate_ldap_user_name(value):
    if not Person.ldap_user_name_valid(value):
        raise ValidationError(_('ldap_user_name_invalid'))
    

    
class LdapConn():

    @classmethod
    def new(cls, ldap_username='', ldap_password=''):
        try:
            connection = ldap.initialize( settings.LDAP_SERVER )
            if ldap_username and ldap_password:
                connection.simple_bind_s( "uid=%s,ou=%s,%s" % ( ldap_username,
                                                                settings.LDAP_PEOPLE,
                                                                settings.LDAP_DN ),
                                          ldap_password )
            else:
                connection.simple_bind_s()
                
            return connection

        except ldap.LDAPError, e:
            logging.error("Could not connect to the Ldap server: '%s'" % settings.LDAP_SERVER )
            logging.error(e)
            raise

    @classmethod
    def new_admin(cls):
        try:
            connection = ldap.initialize( settings.LDAP_SERVER )
            connection.simple_bind_s( "cn=%s,%s" % ( settings.LDAP_ADMIN_USERNAME, settings.LDAP_DN ),
                                      settings.LDAP_ADMIN_USERPASS )
            return connection

        except ldap.LDAPError, e:
            logging.error("Could not connect to the Ldap server: '%s'" % settings.LDAP_SERVER )
            logging.error(e)
            raise

    @classmethod
    def new_user(cls):
        try:
            connection = ldap.initialize( settings.LDAP_SERVER )
            connection.simple_bind_s( "cn=%s,%s" % ( settings.LDAP_USERNAME, settings.LDAP_DN ),
                                      settings.LDAP_USERPASS )
            return connection

        except ldap.LDAPError, e:
            logging.error("Could not connect to the Ldap server: '%s'" % settings.LDAP_SERVER )
            logging.error(e)
            raise
        
        
    @classmethod
    def enable(cls):
        try:
            connection = ldap.initialize( settings.LDAP_SERVER )
            connection.simple_bind_s()
            return True
        except ldap.LDAPError, e:
            return False
        
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

    @classmethod
    def get_from_name(cls,doc_name):
        doc = DocumentType.objects.get(name=doc_name)
        if doc.pk:
            return doc
        else:
            None


    
class Office(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=200, null=False, verbose_name=_('name'))
    
    class Meta:
        db_table = 'offices'
        verbose_name = _('office')
        verbose_name_plural = _('offices')
        ordering = ['name']
        
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
    def members_of(cls, group_cns=[]):
        ldap_condition = ''
        members = []
        for group in group_cns:
            ldap_condition += "(cn=%s)" % group
        if len(group_cns) > 1:
            ldap_condition = "(|%s)" % ldap_condition

        r = LdapConn.new_admin().search_s("ou=%s,%s" %(settings.LDAP_GROUP, settings.LDAP_DN),
                                    ldap.SCOPE_SUBTREE,
                                          ldap_condition, ['memberUid'])
        for dn,entry in r:
            members.append(entry['memberUid'])
        return sum(members,[])


    @classmethod
    def is_member_in_groups(cls,member,groups):
        members = Group.members_of(groups)
        if member in members:
            return True
        else:
            return False
            
    @classmethod
    def add_member_to( cls,  ldap_user_name, group ):
        ldap_group = None
        if 'group_id' in group:
            ldap_group = Group.cn_group_by_gid( group['group_id'] )
        elif 'group_cn' in group:
            ldap_group = group['group_cn']

        if not (ldap_user_name and ldap_group):
            logging.error( "Error updating group '%s' with id '%s' of member: '%s'. Missing parameter.\n" \
                           % (ldap_group,group_id,ldap_user_name) )
            return

        update_group = [( ldap.MOD_ADD, 'memberUid', ldap_user_name )]
        try:
            gdn = "cn=%s,ou=%s,%s" % ( ldap_group,
                                       settings.LDAP_GROUP,
                                       settings.LDAP_DN )
            LdapConn.new_admin().modify_s(gdn, update_group)
            logging.info("Added new member %s in ldap group: %s \n" % (ldap_user_name,ldap_group) )
        except ldap.LDAPError, e:
            logging.error( "Error adding member %s in ldap group: %s \n" % (ldap_user_name,ldap_group) )
            logging.error( e )

            
    @classmethod
    def add_member_in_groups( cls,  ldap_user_name, cn_groups ):
        update_group = [( ldap.MOD_ADD, 'memberUid', ldap_user_name )]
        for group in cn_groups:
            Group.add_member_to(ldap_user_name,{'group_cn': group})

            
    @classmethod
    def remove_member_of( cls,  ldap_user_name, group_id ):
        ldap_group = Group.cn_group_by_gid( group_id )
        if not (ldap_user_name and ldap_group):
            logging.error( "Error deleting group %s of member: %s. Missing parameter.\n" \
                           % (ldap_group,ldap_user_name) )
            return
            
        delete_group = [(ldap.MOD_DELETE , 'memberUid', ldap_user_name )]
        try:
            gdn = "cn=%s,ou=%s,%s" % ( ldap_group,
                                       settings.LDAP_GROUP,
                                       settings.LDAP_DN )
            LdapConn.new_admin().modify_s(gdn,delete_group)
            logging.info("Removed member %s of group %s \n" % (ldap_user_name,ldap_group) )
        except ldap.LDAPError, e:
            logging.error( "Error deleting member %s of group: %s \n" % (ldap_user_name,ldap_group) )
            logging.error( e )

            
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
        return sorted(rows)

    
class Person(models.Model):
    
    document_regex = RegexValidator(regex=r'^\d{6,10}$',
                                    message=_('invalid_value'))

    id = models.AutoField(primary_key=True, null=False)
    name = models.CharField(max_length=200, null=False,
                            verbose_name=_('name'))
    surname = models.CharField(max_length=200,null=False,
                               verbose_name=_('surname'))
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
                                      verbose_name=_('ldap_user_name'),
                                      validators=[validate_ldap_user_name])
    ldap_user_password = models.CharField(max_length=200,
                                          null=True, blank=True,
                                          verbose_name=_('ldap_user_password'),
                                          validators=[validate_ldap_user_password])
    received_application = models.BooleanField(default=False,
                                               verbose_name=_('received_application'))
    group_id = models.IntegerField(null=True, blank=True, verbose_name=_('group_id'))

    
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

    def office_name(self):
        if self.office:
            return self.office.name
        else:
            return self.other_office
    
    @classmethod
    def ldap_fields_map(cls):
        return {'gidNumber': 'group_id',
                'numdoc': 'document_number',
                'sn': 'surname',
                'givenName': 'name',
                'uid': 'ldap_user_name',
                'userPassword': 'ldap_user_password',
                'tipodoc': 'document_type'}

     
    @classmethod
    def ldap_user_name_valid (cls, username):
        if re.match('^[a-z0-9]+$', username ):
            return True
        else:
            return False

        
    @classmethod
    def ldap_password_valid (cls, password):
        if re.match( r'.{8,}([A-Za-z0-9@#$%^&+=]*)', password ):
            return True
        else:
            return False

        
    @classmethod
    def make_secret(cls,password):
        """
        Encodes the given password as a base64 SSHA hash+salt buffer
        Taken from: https://gist.github.com/rca/7217540
        """
        salt = os.urandom(4)

        # hash the password and append the salt
        sha = hashlib.sha1(password)
        sha.update(salt)

        # create a base64 encoded string of the concatenated digest + salt
        digest_salt_b64 = '{}{}'.format(sha.digest(), salt).encode('base64').strip()

        # now tag the digest above with the {SSHA} tag
        tagged_digest_salt = '{{SSHA}}{}'.format(digest_salt_b64)

        return tagged_digest_salt

    
    @classmethod
    def next_ldap_uidNumber(cls):
        ldap_condition = "(uidNumber=*)"
        next_value = 0
        ldap_dn ="ou=%s,%s" %(settings.LDAP_PEOPLE, settings.LDAP_DN)

        r = LdapConn.new_admin().search_s(ldap_dn,ldap.SCOPE_SUBTREE,
                                    ldap_condition,
                                    ['uidNumber'])

        for dn,entry in r:
            if entry['uidNumber'][0] and int(entry['uidNumber'][0]) > next_value:
                next_value = int(entry['uidNumber'][0])

        if next_value > 0:
            next_value += 1

        return next_value

    
    @classmethod
    def exist_ldap_uidNumber(cls, uidnumber):
        ldap_condition = "(uidNumber=%s)" % uidnumber
        ldap_dn ="ou=%s,%s" %(settings.LDAP_PEOPLE, settings.LDAP_DN)

        r = LdapConn.new().search_s(ldap_dn,ldap.SCOPE_SUBTREE,
                                    ldap_condition,
                                    ['uidNumber'])
        for dn,entry in r:
            if int(entry['uidNumber'][0]) == int(uidnumber):
                return True
        return False

    
    @classmethod
    def ldap_uid_by_id(cls, doc_num, type_num, nationality=''):
        nationality = nationality or settings.LDAP_PEOPLE_PAISDOC
        
        ldap_condition = "(&(numdoc=%s)(tipodoc=%s)(paisdoc=%s))" % (doc_num, type_num, nationality)

        r = LdapConn.new().search_s("ou=%s,%s" %(settings.LDAP_PEOPLE, settings.LDAP_DN),
                                    ldap.SCOPE_SUBTREE,
                                    ldap_condition,
                                    ['uid'])
        uids = []
        for dn,entry in r:
            uids.append( entry['uid'][0] )
        return uids

    
    @classmethod
    def exists_in_ldap(cls, uid):
        
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
    def map_ldap_field(cls,ldap_field):
        fields = Person.ldap_fields_map()
        for field in fields:
            if field == ldap_field:
                return fields["%s" % field] 
        return None
        

    
    @classmethod
    def get_from_ldap(cls,uid):
        ldap_condition = "(uid=%s)" % uid
        ldap_person = None
        r = LdapConn.new_admin().search_s("ou=%s,%s" %(settings.LDAP_PEOPLE, settings.LDAP_DN),
                                    ldap.SCOPE_SUBTREE,
                                    ldap_condition)
        for dn,entry in r:
            if entry['uid'][0] == uid:
                ldap_person = Person()
                for field in entry:
                    if not Person.map_ldap_field(field) is None:
                        object_field = Person.map_ldap_field(field)
                        if object_field == 'document_type':
                            setattr(ldap_person,object_field,
                                    DocumentType.get_from_name(entry[field][0]))
                        else:
                            setattr(ldap_person,object_field,str(entry[field][0]))
        return ldap_person

    
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

        
    @classmethod
    def ldap_udn_for( cls, ldap_user_name ):
        return "uid=%s,ou=%s,%s" % ( ldap_user_name,
                                     settings.LDAP_PEOPLE,
                                     settings.LDAP_DN )
        
    def update_ldap_data_from(self,person):
        try:
            update_person = [( ldap.MOD_REPLACE, 'telephoneNumber', str(person.work_phone) or None),
                             ( ldap.MOD_REPLACE, 'physicalDeliveryOfficeName',
                               LdapConn.parseattr(person.office_name()))]
            udn = Person.ldap_udn_for( person.ldap_user_name )
            LdapConn.new_user().modify_s(udn, update_person)
            logging.info( "Updated ldap user data for %s \n" % person.ldap_user_name)
        except ldap.LDAPError, e:
            logging.error( "Error updating ldap user data for %s \n" % person.ldap_user_name)
            logging.error( e )

     
    @classmethod
    def update_ldap_user_password( cls, ldap_user_name, new_password ):
        try:
            update_person = [( ldap.MOD_REPLACE, 'userPassword', new_password )]
            udn = Person.ldap_udn_for( ldap_user_name )
            LdapConn.new_admin().modify_s(udn, update_person)
        except ldap.LDAPError, e:
            logging.error( "Error updating ldap user password for %s \n" % ldap_user_name)
            logging.error( e )

            
    def update_ldap_gidgroup( self, new_group_id ):
        try:
            update_person = [( ldap.MOD_REPLACE, 'gidNumber', new_group_id )]
            udn = Person.ldap_udn_for( self.ldap_user_name )
            LdapConn.new_admin().modify_s(udn, update_person)
            logging.info("Changed group to '%s' for ldap group id '%s'\n" % \
                         (self.ldap_user_name, new_group_id) )
        except ldap.LDAPError, e:
            logging.error( "Error updating ldap user gidGroup '%s' for ldap user '%s' \n" % \
                           (self.ldap_user_name, new_group_id) )
            logging.error( e )
            
            
    @classmethod
    def create_ldap_user( cls,  ldap_user_name, new_ldap_user ):
        if not (ldap_user_name and new_ldap_user):
            logging.error( "Error creating user %s. Missing parameter.\n" % new_ldap_user )
            return
        
        try:
            udn = Person.ldap_udn_for( ldap_user_name )
            res = LdapConn.new_admin().add_s(udn, new_ldap_user)
            logging.info("Created new user in Ldap: %s " % new_ldap_user )
        except ldap.LDAPError, e:
            logging.error( "Error adding ldap user %s \n" % ldap_user_name)
            logging.error( e )

                
@receiver(pre_save, sender=Person)
def update_user_password(sender, instance, *args, **kwargs):
    if instance.pk and instance.pk > 0:  #update!
        current = Person.objects.get(id=instance.pk)
        if current.ldap_user_password != instance.ldap_user_password:
            instance.ldap_user_password = Person.make_secret( instance.ldap_user_password )
    else: # nuevo!
        instance.ldap_user_password = Person.make_secret( instance.ldap_user_password )

        
@receiver(user_logged_in)
def sig_user_logged_in_check(sender, user, request, **kwargs):
    try:
        if settings.LDAP_GROUP_VALIDATION:
            if not Group.is_member_in_groups( str(user),
                                              settings.LDAP_GROUPS_VALID) \
                                              and not request.user.is_superuser:
                logging.warning("The user %s does not have permissions ldap in groups %s" % \
                                (user, settings.LDAP_GROUPS_VALID))
                logout(request)
    except ldap.LDAPError, e:
        logging.error( "Error during authentication with LDAP server for user %s.\n" % user )
        logging.error( e )
        if not request.user.is_superuser:
            logout(request)
