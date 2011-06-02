from django.conf.urls.defaults import *
from django.contrib import admin as django_admin
from django.views.generic.simple import redirect_to

from emark import admin


django_admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', redirect_to, {'url': '/today/'}),
    (r'^today/', include('today.urls')),
    (r'^cal/', include('cal.urls')),

    (r'^rosetta/', include('rosetta.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(django_admin.site.urls)),
    url(r'^settings/', include(admin.site.urls))
)
