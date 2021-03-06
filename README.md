# mollys
Administration request for internal user accounts to the organization. The user accounts are relationated with ldap account

### Package Installation debian stretch
```bash
apt install git
apt install python-dev
apt install python-pip
apt install pkg-config
apt install libpq-dev
apt install libyaml-dev
apt install libldap2-dev
apt install libsasl2-dev
apt install gettext
apt install libjpeg-dev
apt install zlib1g-dev
apt install libgtk2.0-dev
apt install libgirepository1.0-dev
```

### Python lib Installation
```bash
pip install -r requirements.txt
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