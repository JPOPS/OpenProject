from django.db import models
class noteslist(models.Model):
	optype=models.CharField(max_length=30,null=True)
	describe=models.CharField(max_length=300,null=True)
	date=models.CharField(max_length=30,null=True)