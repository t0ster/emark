from django.conf import settings
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^$', 'today.views.index'),
    url(r'^view/(?P<pk>\d+)/$', 'today.views.detail', name='lesson_detail'),
)
