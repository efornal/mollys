# -*- encoding: utf-8 -*-
"""
Django settings for mollys project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from django.utils.translation import ugettext_lazy as _
LANGUAGE_CODE = 'es'
LANGUAGES = (
  ('es', _('Spanish')),
  ('en', _('English')),
)
USE_I18N = True


# LDAP CONFIGURATION ====================\

# LDAP server
LDAP_SERVER = 'ldap://host_ldap:port'

# Dn for entry
LDAP_DN = 'dc=domain,dc=edu,dc=ar'

# LDAP authentication
LDAP_USER_NAME='user_name'
LDAP_USER_PASS='password'

# Organizational Unit for Person and Person Group
LDAP_GROUP  = 'Group' # ou=Entry
LDAP_PEOPLE = 'People' # ou=Entry
LDAP_GROUP_FIELDS  = ['gidNumber','cn']  # id first!
LDAP_PEOPLE_FIELDS = ['uid','cn'] # idfirst!
LDAP_GROUP_MIN_VALUE = 500 # min group_id (group_id>= 500) for ldap search filter
MIN_LENGTH_LDAP_USER_PASSWORD = 8
LDAP_DEFAULT_GROUPS = ['audio','cdrom'] # ldap default groups for each new user

# Params for create new people in ldap
LDAP_PEOPLE_OBJECTCLASSES = ['agente','hordeperson','inetOrgPerson',
                             'organizationalperson','person','posixaccount',
                             'shadowaccount', 'top']
LDAP_PEOPLE_PAISDOC = "ARG"
LDAP_PEOPLE_HOMEDIRECTORY_PREFIX = "/home/"

# =======================================/


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# set static path for production
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'tfp%=#=oszs#x4wea8mkm60p=nmg3l9)jq5g1%s_ev#_4$w#&-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'bootstrap_themes',
    'app',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'mollys.urls'

import os
SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    '/static/',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(SETTINGS_PATH, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mollys.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mollys_db',
        'USER': 'mollys_owner',
        'PASSWORD': 'owner',
        'PORT': '5432',        
        'HOST': 'localhost',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL='/static/'

LOGIN_URL='/login/'

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))


from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

LOCALE_PATHS = (
     BASE_DIR + '/locale', )

# loggin querys in develompent
# if DEBUG:
#     import logging
#     l = logging.getLogger('django.db.backends')
#     l.setLevel(logging.DEBUG)
#     l.addHandler(logging.StreamHandler())
#     logging.basicConfig(
#         level = logging.DEBUG,
#         format = " %(levelname)s %(name)s: %(message)s",
#     )

DEFAULT_CHARSET = 'utf-8'

SUIT_CONFIG = {
    'ADMIN_NAME': _('title')
}

# =================================\
# django ldap configuration

import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

import logging
logger = logging.getLogger('django_auth_ldap')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


AUTH_LDAP_SERVER_URI = LDAP_SERVER

AUTH_LDAP_BIND_DN = "cn=%s,%s" % ( LDAP_USER_NAME, LDAP_DN )
AUTH_LDAP_BIND_PASSWORD = LDAP_USER_PASS

AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=%s,%s" % (LDAP_PEOPLE,LDAP_DN),
                                   ldap.SCOPE_SUBTREE, "(uid=%(user)s)")
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail"
}

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)
# =================================/
