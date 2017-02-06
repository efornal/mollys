from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^people/new',views.new, name='new'),
    url(r'^people/create',views.create, name='create'),
    url(r'^people/print/(\d+)/$',views.print_request, name='print_request'),
    url(r'^$', views.index, name='index'),
    url(r'^set_language', views.set_language, name='set_language'),
    url(r'^admin/person/checkldap',views.check_ldap, name='check_ldap'),
]

