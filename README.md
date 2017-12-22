# mollys
Administration request for internal user accounts to the organization. The user accounts are relationated with ldap account

### Package Installation
```bash
sudo apt-get install python2.7
sudo apt-get install postgresql-9.4
sudo apt-get install python-psycopg2
sudo apt-get install python-pip=1.5.6-5
sudo apt-get install python-yaml=3.11-2
sudo apt-get install python-ldap=2.4.10-1
sudo apt-get install python-dev=2.7.9-1
sudo apt-get install gettext=0.19.3-2
sudo pip install django-suit==0.2.13
sudo pip install django==1.8.5
sudo pip install django-extensions==1.5.5
sudo pip install reportlab==3.2.0
sudo pip install django-bootstrap-themes==3.1.2
sudo pip install django-auth-ldap==1.2.6

```
### Postgres configuration
```bash
createdb mollys_db;
createuser mollys_owner -P;

/etc/postgresql/9.3/main/pg_hba.conf
hostssl  mollys_db     mollys_owner        ::1/128                 password

/etc/init.d/postgresql restart
psql -h localhost -U mollys_owner -p 5432 -d mollys_db
```
### App configuration
descargar archivos:

git clone https://github.com/efornal/mollys.git

cd mollys

cp mollys/settings.tpl.py mollys/settings.py

mkdir static_production

habilitar:

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)


```bash
python manage.py syncdb
python manage.py migrate
django-admin compilemessages

python manage.py collectstatic

python manage.py test  --keepdb
```



### Con apache
```bash
apt-get install apache2 libapache2-mod-wsgi
apt-get install libapache2-mod-python

Crear archivo /etc/apache2/conf-available/django.conf

WSGIScriptAlias /admin /srv/pyapp/mollys/mollys/wsgi.py
WSGIPythonPath /srv/pyapp/mollys/

Alias /static /srv/pyapp/mollys/static
<Directory /srv/pyapp/mollys/mollys>
       <Files wsgi.py>
                Allow from all
        </Files>
</Directory>


a2enconf django
a2ensite default-ssl
service apache2 reload

```


### Showing models
```bash
sudo aptitude install python-pygraphviz

python manage.py graph_models -a -o myapp_models.pdf
```

# permisos en postgres para mollys_user
```bash
# up
GRANT ALL ON ALL TABLES IN SCHEMA public TO mollys_user;
# down
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM mollys_user;


#up
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO mollys_user;
#down
REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM mollys_user;

```