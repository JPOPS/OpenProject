from django.conf.urls import patterns, include, url

from django.contrib import admin
import os
import settings
admin.autodiscover()
root_path = os.path.dirname(globals()["__file__"]) 
urlpatterns = patterns('',
	url(r'^css/(?P<path>.*)$','django.views.static.serve',{'document_root':root_path+settings.css_path}),
	url(r'^js/(?P<path>.*)$','django.views.static.serve',{'document_root':root_path+settings.js_path}),
	url(r'^img/(?P<path>.*)$','django.views.static.serve',{'document_root':root_path+settings.img_path}),
	url(r'^fonts/(?P<path>.*)$','django.views.static.serve',{'document_root':root_path+settings.fonts_path}),
	url(r'^plugins/(?P<path>.*)$','django.views.static.serve',{'document_root':root_path+settings.plugins_path}),		
    url(r'^$', 'index.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login', 'index.views.login', name='login'),
    url(r'^logout', 'index.views.logout', name='logout'),
    url(r'^task/', include('task.urls')),
    url(r'^grap/', include('graphical.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^node/', include('node.urls')),
    url(r'^disp/', include('disp.urls')),
    url(r'^notes/', include('notes.urls')),
)
