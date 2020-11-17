
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	coPI = models.CharField(max_length=100, blank=True, default='')
	member1 = models.CharField(max_length=100, blank=True, default='')
	member2 = models.CharField(max_length=100, blank=True, default='')
	member3 = models.CharField(max_length=100, blank=True, default='')
	member4 = models.CharField(max_length=100, blank=True, default='')
	member5 = models.CharField(max_length=100, blank=True, default='')
	
	#date = models.DateTimeField(auto_now_add=True)
	date = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	#sentiment = 
	#sent = sentiment(self.content)
	#sent = "default"
	#sent = sentiment(str(content))
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk':self.pk})

	
