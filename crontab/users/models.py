from django.db import models
class userslist(models.Model):
	username=models.CharField(max_length=60,null=True)
	email=models.CharField(max_length=100,null=True)