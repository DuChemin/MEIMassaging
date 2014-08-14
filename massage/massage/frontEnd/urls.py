# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('massage.frontEnd.views',
    url(r'^list/$', 'list', name='list'),
    # url(r'^select/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/', 'select'),
    # url(r'^select/$', 'select', name='select'),
    # url(r'^selectTransform/$', 'selectTransform', name='selectTransform'),
    url(r'^metadata/$', 'metadata', name='metadata')
)
