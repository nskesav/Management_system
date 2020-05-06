from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, auth
from django.http import HttpResponseRedirect
from django.contrib import messages
# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import *

test = tt_record.create()

def register(request):
	if request.method == "POST":
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		username = request.POST.get('username');
		password = request.POST.get('password');
		email = request.POST['email']
		if User.objects.filter(username = username).exists():
			messages.info(request,'USERNAME ALREADY EXISTS')
			return redirect('register')
		elif User.objects.filter(email = email).exists():
			messages.info(request,'Email ALREADY EXISTS')
			return redirect('register')
		else:
			user = User.objects.create_user(username = username,first_name = first_name,last_name = last_name,password = password, email = email)
			user.save();
			return redirect('/accounts/land')
	else:
		return render(request,'registration\\registration.html')

def land(request):
	return render(request,'registration\landpage.html')
	

def post_login(request):
	return render(request,'post_login\landing_login.html')
def login_view(request):
	if request.method == "POST":
		postdata = request.POST.copy()
		u = postdata.get('username', '')
		p = postdata.get('password', '')
		user = authenticate(request,username = u,password = p)
		
		if user is not None:
			if user.is_active:
				login(request, user)
				data = time_table.objects.filter(username = user)
				valuesdata = data.values()
				#res = post_login(request,u)
				#return res
				#return redirect('/accounts/post_login/',{'username': u,'ttdata' : data,'uname': user, 'values': valuesdata})
				return render(request,"post_login\landing_login.html",{'ttdata' : data,'uname': user, 'values': valuesdata})
			else:
				request.session['username'] = u
				user.backend = 'django.contrib.auth.backends.ModelBackend'
				user.is_active = True
				user.save()
		else:
			messages.info(request, 'Please Check your Login Credentials')
			return redirect('login')
	else:
		return render(request,'registration\login.html')

def logout_view(request):
	auth.logout(request)
	return render(request,"post_login\logout.html")



	
def slot_confirm(request):
	if request.method == "POST":
		postdata = request.POST.copy()
		sem_section = postdata.get('sem_section', '')
		subject_id = postdata.get('subject_id', '')
		day_name = postdata.get('day_name','')
		hour_no = postdata.get('hour_no','')
	return render(request,'post_login\slot_confirm.html',{'sem_section': sem_section,'subject_id':subject_id,'day_name': day_name,'hour_no':hour_no})