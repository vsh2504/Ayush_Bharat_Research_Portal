from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post,Files 
from users.models import Profile
from .forms import DocumentForm

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