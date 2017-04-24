# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

import views
urlpatterns = patterns('',
	url(r'^interval$', views.hourinterval),
	url(r'^hourscat/(\d+)/$', views.hourscat),
)