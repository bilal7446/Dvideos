from django.db import models
from datetime import datetime   



class Video(models.Model):
	id=models.AutoField(primary_key=True)
	title=models.CharField(max_length=100)
	date=models.DateField(default=datetime.now, blank=True)
	genres=models.CharField(max_length=50)
	thumb=models.ImageField(default='default.jpg',blank=True)
	vid=models.FileField()

	def __str__(self):
		return self.title

# Create your models here.
