# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

import views
urlpatterns = patterns('',
	url(r'^list$', views.nodelist),
	url(r'^add$', views.nodeadd),
	url(r'^edit/(\d+)/$', views.nodeedit),
	url(r'^delete/(\d+)/$', views.nodedelete),
	url(r'^testing$', views.nodetesting),

)