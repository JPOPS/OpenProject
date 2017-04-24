# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import loader,Context
from node.models import nodeslist
from task.models import cronlist
from node.models import cronedition
from notes.views import opnotes
import datetime,time
import paramiko
#文件下载
from django.http import StreamingHttpResponse
##登录模块
from django.contrib import auth
from django.contrib.auth.decorators import login_required
#任务分发页面
@login_required
def distribute(request):
	path='任务分发'
	menuif_0 =1
	menuif_0_1 =1
	editionNum=len(cronedition.objects.all())
	nodeNum=len(nodeslist.objects.all())
	try:
		lastup=cronedition.objects.all().order_by("-id")[0]
	except:
		lastup=None
	info={'editionNum':editionNum,'nodeNum':nodeNum}
	return render_to_response('distribute.html',{'menuif_0':menuif_0,'menuif_0_1':menuif_0_1,'path':path,'info':info,'lastup':lastup})

#生成cron文件
@login_required
def cronfile(request):
	if request.method == 'POST':
		operation = request.POST.get('operation', None)
		if operation == 'create':
			tasklist=cronlist.objects.all().order_by("id")
			#获取当前时间
			date=datetime.datetime.now()
			#版本
			edition=date.strftime("%Y%m%d%H%M%S")
			#更新时间
			updatetime=date.strftime("%Y-%m-%d %H:%M:%S")
			#统计任务数
			crontotal=len(tasklist)
			cronfilepath="/data/crontab/cronfile/%s" % (str(edition))
			f=file(cronfilepath,"a+")
			f.write('#crontab配置文件由XesCron系统生成,共 '+str(crontotal)+' 条任务,更新时间 '+updatetime+'\n\n')
			for task in tasklist:
				Notes='#%s-%s#\n' % (task.personal,task.describe)
				expression="%s\n\n" %(task.expression)
				f.write(Notes.encode("utf-8"))
				f.write(expression.encode("utf-8"))
			f.close()
			#操作完成入库
			cronstate=True
			cronedition.objects.create(edition=edition,updatetime=updatetime,crontotal=crontotal,cronstate=cronstate)
			#写入日志
			optype='生成cron'
			describe='任务数'+str(crontotal)
			date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			opnotes(date,optype,describe)
			return HttpResponse(u"Success")

#分发文件
@login_required
def sendfile(request):
	if request.method == 'POST':
		operation = request.POST.get('operation', None)		
		if operation == 'end':
			cron=cronedition.objects.all().order_by("-id")[0]
			nodes=nodeslist.objects.all()
			for node in	nodes:
				hostname = node.nodeip
				port = int(node.nodeport)
				username = node.nodename
				password = node.nodepass			
				paramiko.util.log_to_file('/data/crontab/logs/paramiko.log')
				client = paramiko.Transport((hostname, port))
				client.connect(username = username, password = password)
				sftp = paramiko.SFTPClient.from_transport(client)
				localpath='/data/crontab/cronfile/%s' % (cron.edition)
				remotepath='/var/spool/cron/root'
				sftp.put(localpath,remotepath)
			client.close()
			#写入日志
			optype='分发cron'
			describe='分发cron文件至各节点'
			date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			opnotes(date,optype,describe)
			return HttpResponse(u"Success")

@login_required
def distributelist(request):
	path='分发记录'
	menuif_0 =1
	menuif_0_2 =1
	distributelist=cronedition.objects.all()
	return render_to_response('distributelist.html',{'menuif_0':menuif_0,'menuif_0_2':menuif_0_2,'path':path,'distributelist':distributelist})

#crontab下载
def download(request,cronfile):
    # do something...

    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    the_file_name = "/data/crontab/cronfile/"+str(cronfile)
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(cronfile)
    return response