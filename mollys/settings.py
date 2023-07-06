# -*- coding: utf-8 -*-
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
import ast
import ldap
import environ
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_URL = os.environ.get('BASE_URL')
APPLICATION_NAME = os.environ.get('APPLICATION_NAME')
APPLICATION_DESC = os.environ.get('APPLICATION_DESC')
# CONFIGURATION FOR PRODUCTION  ====================\
#STATIC_ROOT = os.path.join(BASE_DIR, "mollys/static_produccion")
#STATICFILES_DIRS = (
#    os.path.join(BASE_DIR, "static"),
#)
#STATIC_URL='/mollys/static_production/'
#DEBUG = False

# ==================================================/



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS')

ADMINS = os.environ.get('ADMINS')


MANAGERS = os.environ.get('MANAGERS')


EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "False") == "True"
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "False") == "True"
EMAIL_FROM = os.getenv('EMAIL_FROM')
EMAIL_URL_ADMIN = os.getenv('EMAIL_URL_ADMIN')
EMAIL_RECIPIENT_LIST = ast.literal_eval(os.environ.get('EMAIL_RECIPIENT_LIST'))
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Application definition
INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'jquery',
    'jquery_ui',
    'bootstrap_ui',
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
    'app.middleware.ForceLangMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': os.environ.get('DEBUG'),
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
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD':  os.environ.get('DB_USER_PASSWORD'),
        'PORT': os.environ.get('DB_PORT'),
        'HOST': os.environ.get('DB_HOST'),
    },
    'db_owner': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_OWNER'),
        'PASSWORD': os.environ.get('DB_OWNER_PASSWORD'),
        'PORT': os.environ.get('DB_PORT'),
        'HOST': os.environ.get('DB_HOST'),
    },
}

LANGUAGE_CODE =  os.environ.get('LANGUAGE_CODE')

LANGUAGES = (
  ('es', _('Spanish')),
  ('en', _('English')),
)
USE_I18N = True


ROOT_URLCONF = 'mollys.urls'

STATIC_ROOT = os.environ.get('STATIC_ROOT')
STATIC_URL = os.environ.get('STATIC_URL')

LOGIN_URL = os.environ.get('LOGIN_URL')
LOGIN_REDIRECT_URL = os.environ.get('LOGIN_REDIRECT_URL')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

LOCALE_PATHS = [
    os.path.join(os.environ.get('CONTEXT_PATH'), '/shared/app/locale/'),
    os.path.join(BASE_DIR, 'locale/'),
]

# django configuration
SUIT_CONFIG = {
    'ADMIN_NAME': APPLICATION_NAME
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
TIME_ZONE = os.environ.get('TIME_ZONE')

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_CHARSET =  os.environ.get('DEFAULT_CHARSET')

SESSION_COOKIE_NAME = os.environ.get('SESSION_COOKIE_NAME')
SESSION_COOKIE_PATH = "/"

# LDAP CONFIGURATION ====================\
LDAP_SERVER = os.environ.get('LDAP_SERVER')

LDAP_DN = os.environ.get('LDAP_BIND_DN')

# Organizational Unit for Person
LDAP_PEOPLE = os.environ.get('LDAP_PEOPLE')
LDAP_GROUP  = os.environ.get('LDAP_GROUP')
LDAP_GROUP_FIELDS  = ast.literal_eval(os.environ.get('LDAP_GROUP_FIELDS'))  # id first!
LDAP_PEOPLE_FIELDS = ast.literal_eval(os.environ.get('LDAP_PEOPLE_FIELDS')) # idfirst!

LDAP_DN_AUTH_USERS = os.environ.get('LDAP_DN_AUTH_USERS')
LDAP_DN_AUTH_GROUP = os.environ.get('LDAP_DN_AUTH_GROUP')

LDAP_USERNAME = os.environ.get('LDAP_BIND_USERNAME')
LDAP_PASSWORD = os.environ.get('LDAP_BIND_PASSWORD')
LDAP_ADMIN_USERNAME = os.environ.get('LDAP_BIND_USERNAME')
LDAP_ADMIN_PASSWORD = os.environ.get('LDAP_BIND_PASSWORD')

# Organizational Unit for Person and Person Group
LDAP_GROUP_VALIDATION = os.environ.get('LDAP_GROUP_VALIDATION')
LDAP_GROUPS_VALID   = ast.literal_eval(os.environ.get('LDAP_GROUPS_VALID'))
LDAP_GROUP_MIN_VALUE = os.environ.get('LDAP_GROUP_MIN_VALUE')
LDAP_GROUP_SKIP_VALUES = ast.literal_eval(os.environ.get('LDAP_GROUP_SKIP_VALUES'))

MIN_LENGTH_LDAP_USER_PASSWORD = 8
LDAP_DEFAULT_GROUPS = ast.literal_eval(os.environ.get('LDAP_DEFAULT_GROUPS'))

# Params for create new people in ldap
LDAP_PEOPLE_OBJECTCLASSES = ast.literal_eval(os.environ.get('LDAP_PEOPLE_OBJECTCLASSES'))
LDAP_PEOPLE_PAISDOC = os.environ.get('LDAP_PEOPLE_PAISDOC')
LDAP_PEOPLE_HOMEDIRECTORY_PREFIX = os.environ.get('LDAP_PEOPLE_HOMEDIRECTORY_PREFIX')
LDAP_PEOPLE_LOGIN_SHELL = os.environ.get('LDAP_PEOPLE_LOGIN_SHELL')
#
# Domain name used to identify the institutional mail of an alternative
# Ej: the (LDAP DN)
LDAP_DOMAIN_MAIL=os.environ.get('LDAP_DOMAIN_MAIL')

# =======================================/


# =================================\
# django ldap configuration
#
#
# Ldap Group Type
from django_auth_ldap.config import LDAPSearch, PosixGroupType
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(LDAP_DN_AUTH_GROUP,
                                    ldap.SCOPE_SUBTREE, "(objectClass=posixGroup)"
)
AUTH_LDAP_GROUP_TYPE =  PosixGroupType()
#
#
# User will be updated with LDAP every time the user logs in.
# Otherwise, the User will only be populated when it is automatically created.
AUTH_LDAP_ALWAYS_UPDATE_USER = True
#
#
# Simple group restrictions
# AUTH_LDAP_REQUIRE_GROUP = "cn=users,ou={},{}".format(LDAP_GROUP,LDAP_DN)
# AUTH_LDAP_DENY_GROUP = "cn=denygroup,ou={},{}".format(LDAP_GROUP,LDAP_DN)
#
# Defines the django admin attribute
# according to whether the user is a member or not in the specified group
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_active": "cn=users,{}".format(LDAP_DN_AUTH_GROUP),
    "is_staff": "cn=users,{}".format(LDAP_DN_AUTH_GROUP),
    "is_superuser": "cn=admin,{}".format(LDAP_DN_AUTH_GROUP),
}

AUTH_LDAP_SERVER_URI = LDAP_SERVER

#AUTH_LDAP_BIND_DN = ''
#AUTH_LDAP_BIND_PASSWORD = ''
AUTH_LDAP_USER_SEARCH = LDAPSearch(LDAP_DN_AUTH_USERS,
                                   ldap.SCOPE_SUBTREE, "(uid=%(user)s)")

AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
    "username": "uid",
    "password": "userPassword",
}

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)
# =================================/


# ##loggin querys in develompent
# if DEBUG:
#     import logging
#     l = logging.getLogger('django.db.backends')
#     l.setLevel(logging.DEBUG)
#     l.addHandler(logging.StreamHandler())
#     logging.basicConfig(
#         level = logging.DEBUG,
#         format = " %(levelname)s %(name)s: %(message)s",
#     )

# # Enable debug for ldap server connection
# logger = logging.getLogger('django_auth_ldap')
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.DEBUG)


# #database logging
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#         }
#     },
#     'loggers': {
#         'django.db.backends': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#     }
# }

