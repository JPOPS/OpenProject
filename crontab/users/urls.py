# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

import views
urlpatterns = patterns('',
	url(r'^userlist$', views.userlist),
	url(r'^useradd$', views.useradd),
	url(r'^edit/(\d+)/$', views.useredit),
	url(r'^delete/(\d+)/$', views.userdelete),

)