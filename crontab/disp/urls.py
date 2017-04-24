# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

import views
urlpatterns = patterns('',
	url(r'^list$', views.distributelist),
	url(r'^distribute$', views.distribute),
	url(r'^cronfile$', views.cronfile),
	url(r'^sendfile$', views.sendfile),
	url(r'^download/(.+)/$', views.download),
)