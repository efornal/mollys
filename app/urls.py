from django.conf.urls import patterns, url

from app import views

urlpatterns = patterns('app.views',
    url(r'^people/new','new', name='new'),
    url(r'^people/create','create', name='create'),
    url(r'^people/print/(\d+)/$','print_request', name='print_request'),
    url(r'^$', 'index', name='index'),
    url(r'^set_language', 'set_language', name='set_language'),
    url(r'^admin/person/checkldap','check_ldap', name='check_ldap'),
                       
)
