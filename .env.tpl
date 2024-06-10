## django configuration

LANG=es_AR.UTF-8
TZ=America\/Argentina\/Cordoba

APPLICATION_NAME=Cuenta de usuarios
APPLICATION_DESC=Habilitación de cuenta

DEBUG=True

BASE_URL=https://0.0.0.0:3443

ALLOWED_HOSTS=['*']

ADMINS=(("admin", "admin@domain.com"),)

MANAGERS=(("Manager", "manager@domain.com"),)

SECRET_KEY=thesessionexamplekey

LANGUAGE_CODE=es

DEFAULT_CHARSET=utf-8

TIME_ZONE=America/Argentina/Cordoba

CONTEXT_ROOT=/mollys

CONTEXT_PATH=/srv/mollys

LOGIN_URL=/mollys/login

LOGIN_REDIRECT_URL=/mollys

STATIC_ROOT=/srv/mollys/shared/static

STATIC_URL=/mollys/static/

SESSION_COOKIE_NAME=mollyssessionid

## ldap configuration
LDAP_SERVER=ldap://ldap.domain:389

# autenticacion de usuario del sistema - cardumen
# con permisos de modificacion en las entradas de usuarios
LDAP_BIND_DN=dc=domain,dc=com
LDAP_BIND_USERNAME=mollys
LDAP_BIND_PASSWORD=pass

LDAP_PEOPLE=People
LDAP_GROUP=Group

LDAP_GROUP_FIELDS=["gidNumber","cn"]
LDAP_PEOPLE_FIELDS=["uid","cn"]

LDAP_DN_AUTH_GROUP=ou=Group,dc=domain,dc=com
LDAP_DN_AUTH_USERS=ou=People,dc=domain,dc=com

LDAP_GROUP_VALIDATION=True
LDAP_GROUPS_VALID=["admin","other"]
LDAP_GROUP_MIN_VALUE=500
LDAP_GROUP_SKIP_VALUES=[549]
MIN_LENGTH_LDAP_USER_PASSWORD=8
LDAP_DEFAULT_GROUPS=["users","audio","cdrom"]

LDAP_PEOPLE_OBJECTCLASSES=["agente","hordeperson","inetOrgPerson","organizationalperson","person","posixaccount","shadowaccount","top","extensibleObject"]
LDAP_PEOPLE_PAISDOC="ARG"
LDAP_PEOPLE_HOMEDIRECTORY_PREFIX="/home/"
LDAP_PEOPLE_LOGIN_SHELL="/bin/bash"
LDAP_DOMAIN_MAIL="domain.com"

# =================================/

## database configuration
DB_NAME=mollys_db
DB_USER=mollys_user
DB_USER_PASSWORD=pass
DB_OWNER=mollys_owner
DB_OWNER_PASSWORD=pass
DB_HOST=db
DB_PORT=5432

# email configuration
EMAIL_HOST=email.domain.com
EMAIL_PORT=25
EMAIL_USE_SSL=False
EMAIL_USE_TLS=False
EMAIL_FROM=mollys@domain.com
EMAIL_RECIPIENT_LIST=["email@domain.com"]
EMAIL_URL_ADMIN=https://url_to_admin
