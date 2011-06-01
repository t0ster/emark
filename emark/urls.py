from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import redirect_to

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', redirect_to, {'url': '/today/'}),
    (r'^today/', include('today.urls')),
    (r'^cal/', include('cal.urls')),

    (r'^rosetta/', include('rosetta.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls), name="admin")
)
