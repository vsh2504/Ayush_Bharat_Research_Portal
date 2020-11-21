
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	PI = models.CharField(max_length=100, blank=True, default='')
	coPI = models.CharField(max_length=100, blank=True, default='')
	member1 = models.CharField(max_length=100, blank=True, default='')
	member2 = models.CharField(max_length=100, blank=True, default='')
	member3 = models.CharField(max_length=100, blank=True, default='')
	member4 = models.CharField(max_length=100, blank=True, default='')
	member5 = models.CharField(max_length=100, blank=True, default='')
	funding = models.DecimalField(decimal_places=2,max_digits=15)
	sanctionedAmount = models.DecimalField(decimal_places=2,max_digits=15)
	startDate = models.DateField() 
	endDate = models.DateField()
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

	
class Files(models.Model):
	file_title = models.CharField(max_length=100)
	description = models.CharField(max_length=255, blank=True)
	document = models.FileField(upload_to='documents/')
	project = models.ForeignKey(Post,related_name='files',on_delete=models.CASCADE)
	uploaded_at = models.DateTimeField(auto_now_add=True)

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
