from django.conf.urls import patterns, url

from app import views

urlpatterns = patterns('app.views',
    url(r'^people/new','new', name='new'),
    url(r'^people/create','create', name='create'),
    url(r'^people/outcome','outcome', name='outcome'),
    url(r'^$', 'index', name='index'),
)
