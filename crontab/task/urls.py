# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

import views
urlpatterns = patterns('',
	url(r'^tasklist$', views.tasklist),
	url(r'^addtask$', views.addtask),
	url(r'^addstask$', views.addstask),
	url(r'^errorlist$', views.errorlist),
	url(r'^recycle$', views.recycle),
	url(r'^reedit/(\d+)/$', views.reedit),
	url(r'^redelete/(\d+)/$', views.redelete),
	url(r'^redeleteall$', views.redeleteall),
	url(r'^checke/(\d+)/$', views.checke),
	url(r'^edit/(\d+)/$', views.edit),
	url(r'^delete/(\d+)/$', views.delete),
	url(r'^download$', views.download),
	url(r'^taskxls$', views.taskxls),
	url(r'^downlogs$', views.downlogs),


)