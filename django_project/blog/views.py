from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post,Files,Event 
from users.models import Profile
from .forms import DocumentForm,EventForm
import datetime
from datetime import timedelta
from django.views import generic
from django.utils.safestring import mark_safe
from .utils import Calendar
import calendar
from django.urls import reverse

def home(request):
	#return HttpResponse('<h1>Blog Home</h1>')
	context = {
		#'posts': posts
		'posts': Post.objects.all()
	}
	return render(request, 'blog/home.html',context)

def welcome(request):
	context={

	}
	return render(request, 'blog/welcome.html',context)

class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'
	context_object_name = 'posts'
	ordering = ['-date']
	paginate_by = 6

class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html'
	context_object_name = 'posts'
	
	paginate_by = 6

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date')

class MyPostListView(LoginRequiredMixin, ListView):
	"""docstring for MyPostListView"""
	model = Post
	template_name = 'blog/my_posts.html'
	context_object_name = 'posts'
	paginate_by = 1
	def get_queryset(self):
		user = self.request.user
		return Post.objects.filter(author=user).order_by('-date')

		

class PostDetailView(DetailView):
	model = Post

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super().get_context_data(**kwargs)
		# Add in a QuerySet of all the books
		context['file_obj_list'] = Files.objects.filter(project=context["post"])
		return context


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title','PI','coPI','member1', 'member2','member3','member4','member5', 'content','funding','sanctionedAmount','startDate','endDate']

	# def get_form(self):
	# 	form = super(PostCreateView, self).get_form(form_class)
	# 	form.fields['startDate'].widget.attrs.update({'class': 'datepicker'})
	# 	return form

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title','coPI','member1', 'member2','member3','member4','member5', 'content']

	def form_valid(self, form):
		#form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		validnames = []
		validnames.append(post.PI)
		validnames.append(post.coPI)
		validnames.append(post.member1)
		validnames.append(post.member2)
		validnames.append(post.member3)
		validnames.append(post.member4)
		validnames.append(post.member5)

		if self.request.user == post.author or self.request.user.username in validnames:
			return True
		return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'
	def test_func(self):
		post = self.get_object()

		if self.request.user == post.author:
			return True
		return False

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blog-home')
    else:
        form = DocumentForm()
    return render(request, 'blog/model_form_upload.html', {
        'form': form
    })

class CalendarView(generic.ListView):
    model = Event
    template_name = 'blog/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return datetime.date(year, month, day=1)
    return datetime.date.today()
def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'blog/event.html', {'form': form})