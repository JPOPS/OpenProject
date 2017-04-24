#!/usr/bin/python 
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import loader,Context
from notes.models import noteslist
import datetime,time
##登录模块
from django.contrib import auth
from django.contrib.auth.decorators import login_required

#操作日志列表
@login_required		
def oplist(request):
	path='操作日志'
	menuif_4 =1
	menuif_4_1 =1
	notes=noteslist.objects.all().order_by("-id")
	return render_to_response('noteslist.html',{'menuif_4':menuif_4,'menuif_4_1':menuif_4_1,'path':path,'notes':notes})

#写入日志
def opnotes(date,optype,describe):
	try:
		noteslist.objects.create(date=date,optype=optype,describe=describe)
		return True
	except:
		return False
