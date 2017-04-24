# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import loader,Context
from task.models import cronlist
from task.models import recyclelist
from node.models import nodeslist
from users.models import userslist
from notes.views import opnotes
from node.views import testing
import datetime,time
#文件下载
from django.http import StreamingHttpResponse
#远程登陆
import paramiko
import xlwt
##登录模块
from django.contrib import auth
from django.contrib.auth.decorators import login_required


#添加任务
@login_required
def addtask(request):
	menuif_2 =1
	menuif_2_1 =1
	menuif_2_1_1 =1
	users=userslist.objects.all().order_by("id")
	path='添加任务'
	if request.method == 'POST':
		cronid=request.POST.get('id', None)
		personal=request.POST['personal']
		describe=request.POST['describe']
		expression=request.POST['expression']
		if cronid == None:
			cronlist.objects.create(personal=personal,describe=describe,expression=expression)
			#写入日志
			optype='步骤添加'
			describe=describe
			date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			opnotes(date,optype,describe)			
			return HttpResponseRedirect('/task/tasklist')
		else:
			cronlist.objects.filter(id=cronid).update(personal=personal,describe=describe,expression=expression)
			#写入日志
			optype='任务修改'
			describe=str(cronid)+describe
			date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			opnotes(date,optype,describe)
			return HttpResponseRedirect('/task/checke/'+str(cronid))
	else:
		alert="alert-success hide-default"		
		return render_to_response('addtask.html',{'menuif_2':menuif_2,'menuif_2_1':menuif_2_1,'menuif_2_1_1':menuif_2_1_1,'path':path,'alert':alert,'users':users})


#批量添加任务
@login_required
def addstask(request):
	menuif_2 =1
	menuif_2_1 =1
	menuif_2_1_2 =1
	path='批量添加任务'
	count=0	
	if request.method == 'POST':
		#获取前台数据
		batchtask=request.POST.get('batchtask', None)
		#按\n分隔符分割字符串为数组
		batchtasks = batchtask.split('\n')
		batchtasks2 = batchtask.split('\n')
		#挑出空行
		for i in range(len(batchtasks)):
			if len(batchtasks[i]) < 4:
				batchtasks2.remove(batchtasks[i])
		#区分注释和crontab表达式
		print batchtasks2
		for line in batchtasks2:
			if line.find("#") == 0 :
				#去除\r字符
				Notes=line.replace("#","").replace("\r","")
				Note = Notes.split('-')
				personal=Note[0]
				describe=Note[1]
			else:
				count+=1
				expression=line.replace("\r","")
				cronlist.objects.create(personal=personal,describe=describe,expression=expression)
		#写入日志
		optype='批量添加'
		describe='批量添加数：'+str(count)
		date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		opnotes(date,optype,describe)										
		return HttpResponseRedirect('/task/tasklist')
	else:	
		return render_to_response('addstask.html',{'menuif_2':menuif_2,'menuif_2_1':menuif_2_1,'menuif_2_1_2':menuif_2_1_2,'path':path})



#任务列表详情
@login_required
def tasklist(request):
	menuif_2 =1
	menuif_2_2 =1
	path='任务列表'
	tasklist=cronlist.objects.all().order_by("-id")
	tashNum=len(tasklist)
	return render_to_response('tasklist.html',{'menuif_2':menuif_2,'menuif_2_2':menuif_2_2,'path':path,'tasklist':tasklist,'tashNum':tashNum})
#异常任务详情
@login_required
def errorlist(request):
	menuif_2 =1
	menuif_2_2 =1
	path='异常列表'
	return render_to_response('tasklist.html',{'menuif_2':menuif_2,'menuif_2_2':menuif_2_2,'path':path})
#查看任务详情
@login_required
def checke(request,a):
	menuif_2 =1
	menuif_2_2 =1
	path='任务详情'
	cron=cronlist.objects.filter(id=a)
	return render_to_response('checke.html',{'menuif_2':menuif_2,'menuif_2_2':menuif_2_2,'path':path,'cron':cron[0]})
#编辑任务详情
@login_required	
def edit(request,a):
	menuif_2 =1
	menuif_2_2 =1
	path='编辑任务'
	cron=cronlist.objects.filter(id=a)
	return render_to_response('edit.html',{'menuif_2':menuif_2,'menuif_2_2':menuif_2_2,'path':path,'cron':cron[0]})
#删除到回收站
@login_required
def delete(request,a):
	cron=cronlist.objects.get(id=a)
	date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	recyclelist.objects.create(id=cron.id,personal=cron.personal,describe=cron.describe,expression=cron.expression,date=date)
	cronlist.objects.get(id=a).delete()
	#写入日志
	optype='删除到回收站'
	describe=str(cron.id)+cron.personal
	date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	opnotes(date,optype,describe)	
	return HttpResponseRedirect('/task/tasklist')
#回收站
@login_required
def recycle(request):
	menuif_2 =1
	menuif_2_3 =1
	path='任务回收站'
	tasklist=recyclelist.objects.all()
	return render_to_response('recycle.html',{'menuif_2':menuif_2,'menuif_2_3':menuif_2_3,'path':path,'tasklist':tasklist})

#恢复任务
@login_required
def reedit(request,a):
	menuif_2 =1
	menuif_2_3 =1
	path='恢复任务'
	if request.method == 'POST':
		path='任务回收站'
		cronid=request.POST.get('id', None)
		personal=request.POST['personal']
		describe=request.POST['describe']
		expression=request.POST['expression']
		cronlist.objects.create(id=cronid,personal=personal,describe=describe,expression=expression)
		recyclelist.objects.get(id=a).delete()
		#写入日志
		optype='恢复任务'
		describe=str(cron.id)+cron.personal
		date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		opnotes(date,optype,describe)		
		return HttpResponseRedirect('/task/recycle')
	cron=recyclelist.objects.get(id=a)
	return render_to_response('reedit.html',{'menuif_2':menuif_2,'menuif_2_3':menuif_2_3,'path':path,'cron':cron})

#永久删除
@login_required
def redelete(request,a):
	menuif_2 =1
	menuif_2_3 =1
	path='任务回收站'
	cron=recyclelist.objects.get(id=a)
	recyclelist.objects.get(id=a).delete()
	#写入日志
	optype='永久删除'
	describe=str(cron.id)+cron.personal
	date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	opnotes(date,optype,describe)		
	return HttpResponseRedirect('/task/recycle')

#清空回收站
@login_required
def redeleteall(request):
	recyclelist.objects.all().delete()
	#写入日志
	optype='清空回收站'
	describe='清空回收站'
	date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	opnotes(date,optype,describe)	
	return HttpResponseRedirect('/task/recycle')


@login_required
def taskxls(request):
    tasklist=cronlist.objects.all().order_by("id")
    Cronfile=xlwt.Workbook()
    sheet=Cronfile.add_sheet('sheet 1')
    taskid='任务ID'
    personal='负责人/部门'
    describe='功能描述'
    expression='Cron表达式'
    sheet.write(0,0,taskid.decode('utf-8'))
    sheet.write(0,1,personal.decode('utf-8'))
    sheet.write(0,2,describe.decode('utf-8'))
    sheet.write(0,3,expression.decode('utf-8'))
    row=1
    for task in tasklist:
        sheet.write(row,0,task.id)
        sheet.write(row,1,task.personal)
        sheet.write(row,2,task.describe)
        sheet.write(row,3,task.expression)
        row+=1
    Cronfile.save("/data/crontab/cronfile/XesCron.xls")
    file=download("/data/crontab/cronfile/","XesCron.xls")
    return  file

@login_required
def downlogs(request):
	if request.method == 'POST':
		#获取前台数据
		file_name=request.POST.get('logname', None)	
		nodes=nodeslist.objects.all().order_by("id")
		for node in nodes:
			#判断主节点
			if testing(request,node.id) == 'Success1':
				hostname = node.nodeip
				port = int(node.nodeport)
				username = node.nodename
				password = node.nodepass			
				paramiko.util.log_to_file('/data/crontab/logs/paramiko.log')
				client = paramiko.Transport((hostname, port))
				client.connect(username = username, password = password)
				sftp = paramiko.SFTPClient.from_transport(client)
				localpath='/home/crontablogs/%s' % file_name
				remotepath='/home/crontablogs/%s' % file_name
				print remotepath
				#拉取文件
				try:
					sftp.get(localpath,remotepath)
					client.close()
					break
				except:
					return HttpResponse(u"没有该日志文件")
		#下载日志文件
		try:
			file_path='/home/crontablogs/'		
			logsfile=download(file_path,file_name)
			return logsfile
		except:
			return HttpResponse(u"没有该日志文件")
	else: 
		return HttpResponseRedirect('/task/tasklist/')







#下载日志
def download(file_path,file_name):
    # do something...

    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    the_file = str(file_path)+str(file_name)
    response = StreamingHttpResponse(file_iterator(the_file))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    return response

