# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import loader,Context
from task.models import cronlist
##登录模块
from django.contrib import auth
from django.contrib.auth.decorators import login_required
@login_required
def hourinterval(request):
	menuif_3 =1
	menuif_3_1 = 1
	path='图表统计'
	tasklist=cronlist.objects.all()
	hours=[]
	hourspt1=[]
	hourspt2=[]
	hourspt3=[]
	for cron in tasklist:
		hoursdata=cron.expression.split(' ')[1]
		try:
			hours.append(int(hoursdata))
		except:
			continue
	hoursNum=len(hours)
	for hour in range(0,8):
		count=hours.count(hour)
		if count > 0:
			hourspt1.append([hour,count,format(float(count)/hoursNum, '.2%')])
	for hour in range(8,16):
		count=hours.count(hour)
		if count > 0:
			hourspt2.append([hour,count,format(float(count)/hoursNum, '.2%')])
	for hour in range(16,24):
		count=hours.count(hour)
		if count > 0:
			hourspt3.append([hour,count,format(float(count)/hoursNum, '.2%')])
	return render_to_response('hourinterval.html',{'menuif_3':menuif_3,'menuif_3_1':menuif_3_1,'path':path,'hourspt1':hourspt1,'hourspt2':hourspt2,'hourspt3':hourspt3})

@login_required
def hourscat(request,hour):
	menuif_3 =1
	menuif_3_1 = 1
	path=str(hour)+'点任务执行表'
	hours=[]
	tasklist=cronlist.objects.all()
	for cron in tasklist:
		hoursdata=cron.expression.split(' ')[1]
		try:
			if int(hour)==int(hoursdata):
				hours.append(cron)
		except:
			continue
	return render_to_response('hourslist.html',{'menuif_3':menuif_3,'menuif_3_1':menuif_3_1,'path':path,'hours':hours})			