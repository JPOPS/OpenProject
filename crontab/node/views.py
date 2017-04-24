#!/usr/bin/python 
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
##登录模块
from django.contrib import auth
from django.contrib.auth.decorators import login_required

#节点添加
@login_required
def nodeadd(request):
	path='节点添加'
	menuif_1 =1
	menuif_1_1 =1
	if request.method == 'POST':
		nodeid=request.POST.get('id', None)
		nodeip=request.POST.get('nodeip', None)
		nodename=request.POST.get('nodename', None)
		nodepass=request.POST.get('nodepass', None)
		nodeport=request.POST.get('nodeport', None)
		if nodeid == None:
			nodeslist.objects.create(nodeip=nodeip,nodename=nodename,nodepass=nodepass,nodeport=nodeport)
			#写入日志
			optype='节点添加'
			describe=nodeip
			date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			opnotes(date,optype,describe)			
			return HttpResponseRedirect('/node/list')
		else:
			nodeslist.objects.filter(id=nodeid).update(nodeip=nodeip,nodename=nodename,nodepass=nodepass,nodeport=nodeport)
			#写入日志
			optype='节点修改'
			describe=nodeip
			date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			opnotes(date,optype,describe)			
			return HttpResponseRedirect('/node/list')
	else:
		return render_to_response('nodeadd.html',{'menuif_1':menuif_1,'menuif_1_1':menuif_1_1,'path':path})
#节点列表
@login_required		
def nodelist(request):
	path='节点列表'
	menuif_1 =1
	menuif_1_2 =1
	nodestate=[]
	nodes=nodeslist.objects.all().order_by("id")
	for node in nodes:
		nodestate.append([node.id,'None'])
	return render_to_response('nodelist.html',{'menuif_1':menuif_1,'menuif_1_2':menuif_1_2,'path':path,'nodes':nodes,'nodestate':nodestate})

#节点修改
@login_required
def nodeedit(request,id):
	path='节点修改'
	menuif_1 =1
	menuif_1_1 =1
	node=nodeslist.objects.get(id=id)
	return render_to_response('nodeedit.html',{'menuif_1':menuif_1,'menuif_1_1':menuif_1_1,'path':path,'node':node})
#节点删除
@login_required
def nodedelete(request,id):
	node=nodeslist.objects.get(id=id)
	nodeslist.objects.get(id=id).delete()
	#写入日志
	optype='节点删除'
	describe=node.nodeip
	date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	opnotes(date,optype,describe)	
	return HttpResponseRedirect('/nodes/list')


#带有节点测试节点列表
@login_required		
def nodetesting(request):
	path='节点列表'
	menuif_1 =1
	menuif_1_2 =1
	nodestate=[]
	nodes=nodeslist.objects.all().order_by("id")
	for node in nodes:
		nodestate.append([node.nodeip,testing(request,node.id)])
	print nodestate
	return render_to_response('nodelist.html',{'menuif_1':menuif_1,'menuif_1_2':menuif_1_2,'path':path,'nodes':nodes,'nodestate':nodestate})

@login_required
def testing(request,id):
	try:	
		nodes=nodeslist.objects.get(id=id)
		server_ip = nodes.nodeip
		server_port = int(nodes.nodeport)
		server_user = nodes.nodename
		server_passwd = nodes.nodepass
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(server_ip, server_port,server_user, server_passwd)		
		paramiko.util.log_to_file('/data/crontab/logs/paramiko.log')
		command='ps x |grep crond |grep -v grep -c'
		stdin, stdout, stderr = ssh.exec_command(command)
		err = stderr.readline()
		out = stdout.readline()
		#if "" != err:
		#  #print "command: " + command + " exec failed!\nERROR :" + err
		#  #return true, err
		#  return "failed"
		#else:
		#  #print "command: " + command + " exec success."
		ssh.close()
		return "Success"+str(out.replace("\n",""))
	except:
		ssh.close()
		return "failed"
	