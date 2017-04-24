#!/usr/bin/env python
#coding:utf-8
import datetime,time
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import loader,Context
from node.models import nodeslist
from task.models import cronlist
from node.models import cronedition
##登录模块
from django.contrib import auth
from django.contrib.auth.decorators import login_required
# 主页
@login_required
def index(request):
	menuif_0 = 1
	path='首页'
	#提示语判断
	hours=int(datetime.datetime.now().strftime("%H"))
	if hours >= 0 and hours < 6:
		greeting ='早点休息别熬夜'
	elif hours >= 6 and hours < 12:
		greeting ='早上好'
	elif hours >= 12 and hours <= 23:
		greeting ='下午好'
	#信息统计	
	cronNum=len(cronlist.objects.all())
	nodeNum=len(nodeslist.objects.all())
	editionNum=len(cronedition.objects.all())
	#运行时间
	d1 = datetime.datetime(2017, 4, 24)
	d2 = datetime.datetime(time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday)
	Runningtime=(d2 - d1).days
	info={'cronNum':cronNum,'nodeNum':nodeNum,'editionNum':editionNum,'Runningtime':Runningtime}
	return render_to_response('index.html',{'menuif_0 ':menuif_0 ,'path':path,'greeting':greeting,'info':info})

##登录
def login(request):
	if request.method == 'POST':
		username=request.POST['username']
		password=request.POST['password']
		nextpag=request.POST.get('next', None)
		if nextpag=='':
			nextpag='/'
		print nextpag
		user = auth.authenticate(username=username, password=password)
		if user:
			auth.login(request, user)
			response = HttpResponseRedirect(nextpag)
			response.set_cookie('username',username,3600)
			return response
		else:
			info={'username':username,'error':'用户名或密码错误，请重新输入!'}
			return render_to_response('login.html',{'info':info,'nextpag':nextpag})
	else:
		try:
			nextpag=request.GET['next']
			return render_to_response('login.html',{'nextpag':nextpag})
		except:	
			return render_to_response('login.html')
##注销
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/login?next=/')