# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import loader,Context
from users.models import userslist
from notes.views import opnotes
import datetime,time
##登录模块
from django.contrib import auth
from django.contrib.auth.decorators import login_required

#用户列表
@login_required	
def userlist(request):
	path='用户列表'
	menuif_5 =1
	menuif_5_1 =1
	users=userslist.objects.all().order_by("id")	
	return render_to_response('userlist.html',{'menuif_5':menuif_5,'menuif_5_1':menuif_5_1,'path':path,'users':users})
#添加用户
@login_required	
def useradd(request):
	path='添加用户'
	menuif_5 =1
	menuif_5_1 =1
	if request.method == 'POST':
		userid=request.POST.get('id', None)
		username=request.POST['username']
		email=request.POST['email']
		if userid == None:
			userslist.objects.create(username=username,email=email)
			#写入日志
			optype='添加用户'
			describe=username
			date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			opnotes(date,optype,describe)
			return HttpResponseRedirect('/users/userlist')
		else:
			userslist.objects.filter(id=userid).update(username=username,email=email)
			#写入日志
			optype='修改用户'
			describe=username
			date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			opnotes(date,optype,describe)
			return HttpResponseRedirect('/users/userlist')
	else:
		return render_to_response('useradd.html',{'menuif_5':menuif_5,'menuif_5_1':menuif_5_1,'path':path})
#修改用户
@login_required	
def useredit(request,id):
	path='修改用户'
	menuif_5 =1
	menuif_5_1 =1
	users=userslist.objects.get(id=id)
	return render_to_response('useredit.html',{'menuif_5':menuif_5,'menuif_5_1':menuif_5_1,'path':path,'users':users})

#删除用户
@login_required	
def userdelete(request,id):
	menuif_5 =1
	menuif_5_1 =1
	users=userslist.objects.get(id=id)
	userslist.objects.get(id=id).delete()
	#写入日志
	optype='删除用户'
	describe=users.username
	date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	opnotes(date,optype,describe)
	return HttpResponseRedirect('/users/userlist')