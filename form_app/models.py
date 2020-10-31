from django.db import models

# Create your models here.


class US(models.Model):
	video_id = models.CharField(max_length=200)
	channel_title = models.CharField(max_length=200)
	publish_time = models.CharField(max_length=200)
	category_id = models.CharField(max_length=200)
	tags = models.CharField(max_length=200)

	def __str__(self):
		return self.first_name + ' ' + self.last_name 
