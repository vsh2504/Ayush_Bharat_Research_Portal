from django.shortcuts import render, redirect
#from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm,ContactsUpdateForm
from .models import Profile

import re

# Create your views here.

def register(request):
	if request.method == 'POST':
		#form = UserCreationForm(request.POST)
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'your Account has been created! you can now login!')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html',{'form': form})
	
@login_required
def profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, 
				request.FILES,instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'your Account has been updated!')
			return redirect('profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
	
	context = {
		'u_form':u_form,
		'p_form':p_form
	}
	return render(request,'users/profile.html',context)

@login_required
def Contacts(request):
	user_obj = str(request.user.profile.contacts_list)
	clist = re.split('([A-Za-z  : ]+[+]?[\d]+)',user_obj)
	user_contacts_list = []
	for i in clist:
		if(i!='\r\n' and i!=""):
			user_contacts_list.append(i)
	print(user_contacts_list)
	user_info = request.user
	contacts_dict = { "user_contacts_list":user_contacts_list,"user_info":user_info, }
	return render(request,'users/contacts_list.html',context=contacts_dict)

def updateContacts(request):
	if request.method == 'POST':
		p_form = ContactsUpdateForm(request.POST, 
				request.FILES,instance=request.user.profile)
		if p_form.is_valid():
			p_form.save()
			messages.success(request, f'your Account has been updated!')
			return redirect('my-contacts')
	else:
		p_form = ContactsUpdateForm(instance=request.user.profile)
	
	context = {
		'p_form':p_form
	}
	return render(request,'users/contacts_update.html',context)



 