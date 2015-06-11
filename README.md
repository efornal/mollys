# mollys
Administration request for internal user accounts to the organization


### Package Installation
```bash
sudo apt-get install python2.7
sudo apt-get install postgresql-9.3
sudo apt-get install python-psycopg2
sudo apt-get install python-pip
sudo apt-get install python-yaml
sudo pip install django-suit
sudo pip install django==1.7.4
sudo pip install django-extensions
pip install reportlab
pip install django-bootstrap-themes
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
```bash
python manage.py syncdb
python manage.py migrate
```
