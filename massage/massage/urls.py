# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = patterns('',
    (r'^', include('massage.frontEnd.urls')),
#    (r'^$', RedirectView.as_view(url='/massage/frontEnd/list/')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
