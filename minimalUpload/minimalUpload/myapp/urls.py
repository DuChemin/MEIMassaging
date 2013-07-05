# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('minimalUpload.myapp.views',
    url(r'^list/$', 'list', name='list'),
    url(r'^process/(\d{4})/(\d{2})/(\d{2})/', 'process'),
)
