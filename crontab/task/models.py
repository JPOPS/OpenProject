from django.db import models
class cronlist(models.Model):
	personal=models.CharField(max_length=30,null=True)
	describe=models.CharField(max_length=300,null=True)
	expression=models.CharField(max_length=600,null=True)
class recyclelist(models.Model):
	id = models.IntegerField(primary_key=True)
	personal=models.CharField(max_length=30,null=True)
	describe=models.CharField(max_length=300,null=True)
	expression=models.CharField(max_length=600,null=True)
	date=models.CharField(max_length=30,null=True)


#class recyclelist(models.Model):
#	id = models.IntegerField(primary_key=True)
#	personal=models.CharField(max_length=30,null=True)
#	describe=models.CharField(max_length=300,null=True)
#	crontime=models.CharField(max_length=30,null=True)
#	scripttype=models.CharField(max_length=60,null=True)
#	path=models.CharField(max_length=100,null=True)
#	parameter=models.CharField(max_length=60,null=True)
#	logs=models.CharField(max_length=100,null=True)
#	date=models.CharField(max_length=30,null=True)



#	class cronlist(models.Model):
#	personal=models.CharField(max_length=30,null=True)
#	describe=models.CharField(max_length=300,null=True)
#	crontime=models.CharField(max_length=30,null=True)
#	scripttype=models.CharField(max_length=60,null=True)
#	path=models.CharField(max_length=100,null=True)
#	parameter=models.CharField(max_length=60,null=True)
#	logs=models.CharField(max_length=100,null=True)
