from django.conf.urls import include, url
from django.contrib import admin

from django.conf.urls.i18n import i18n_patterns
urlpatterns = [
    # Examples:
    # url(r'^$', 'mollys.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('app.urls')),
]

urlpatterns += i18n_patterns(
    url(r'^', include('app.urls')),
)
