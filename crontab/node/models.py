from django.db import models
class nodeslist(models.Model):
	nodeip=models.CharField(max_length=100)
	nodename=models.CharField(max_length=30,null=True)
	nodepass=models.CharField(max_length=30,null=True)
	nodeport=models.CharField(max_length=30,null=True)

class cronedition(models.Model):
	edition=models.CharField(max_length=100)
	updatetime=models.CharField(max_length=60,null=True)
	crontotal=models.IntegerField(max_length=60,null=True)
	cronstate=models.NullBooleanField(null=True)