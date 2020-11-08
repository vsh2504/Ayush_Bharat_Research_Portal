
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
#import numpy as np
#from textblob import TextBlob



# Create your models here.
'''
analysis=TextBlob("i  hate people")
if analysis.sentiment.polarity>0 :
    print("positive")
elif analysis.sentiment.polarity==0 :
    print("neutral")
else :
    print("negative")
'''



class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
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

	
