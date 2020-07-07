from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, auth
from django.http import HttpResponseRedirect
from django.contrib import messages
# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import date,timedelta
import calendar
from django.core.exceptions import ObjectDoesNotExist

#test = tt_record.create()

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
	
@login_required(login_url='/accounts/login')
def post_login(request):
	user = request.user
	data = time_table.objects.filter(username = user)
	print(data)
	datetimetoday = date.today()
	start = datetimetoday - timedelta(days=datetimetoday.weekday())
	end = start + timedelta(days=6)
	daysrange = []
	delta = end - start       # as timedelta
	for i in range(delta.days ):
  	  day = start + timedelta(days=i)
  	  #print(str(day))
  	  daysrange.append(str(day))
	#print(daysrange)
	daysdict = dict(zip(calendar.day_name,daysrange))
	to_be_deleted = []
	for i in data:
		try:
			classes = tt_record.objects.select_related('tt').filter(date = daysdict[str(i.day_name)],tt_id = i.id,is_rescheduled = False).get(tt_id = i.id)
			print(classes)
		except ObjectDoesNotExist:
			to_be_deleted.append(i.id)
			data = data.exclude(id__in=to_be_deleted)
			print("COULDNT FIND YA") 
	#print(finaldata)
	valuesdata = data.values('day_name_id')
	print(valuesdata)
	#classes = tt_record.objects.select_related('tt')
	#print(classes)
	#res = post_login(request,u)
	#return res
	#return redirect('/accounts/post_login/',{'username': u,'ttdata' : data,'uname': user, 'values': valuesdata})
	resc_classes = rescheduled_classes.objects.filter(resc_date__gte = datetimetoday,resc_username = user)

	resc_classes_values  = resc_classes.values('resc_date')
	print(resc_classes,resc_classes_values)
	daynametoday = datetimetoday.strftime("%A")
	return render(request,"post_login\landing_login.html",{"resc_classes": resc_classes,"daysdict": daysdict,'ttdata' : data ,'uname': user,'date':datetimetoday,'dayname': daynametoday, 'values': valuesdata})
	#return render(request,"post_login\landing_login.html")

def login_view(request):
	if request.method == "POST":
		postdata = request.POST.copy()
		u = postdata.get('username', '')
		p = postdata.get('password', '')
		user = authenticate(request,username = u,password = p)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/accounts/post_login')
				# data = time_table.objects.filter(username = user)
				# print(data)
				# valuesdata = data.values('day_name_id')
				# print(valuesdata)
				# classes = tt_record.objects.select_related('tt')
				# #print(classes)
				# #res = post_login(request,u)
				# #return res
				# #return redirect('/accounts/post_login/',{'username': u,'ttdata' : data,'uname': user, 'values': valuesdata})
				# datetimetoday = date.today()
				# daynametoday = datetimetoday.strftime("%A")
				# return render(request,"post_login\landing_login.html",{'ttdata' : data,'uname': user,'date':datetimetoday,'dayname': daynametoday, 'values': valuesdata,'classes': classes})
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



@login_required(login_url='/accounts/login')
def slot_confirm(request):
	if request.method == "POST":
		postdata = request.POST.copy()
		curr_id = postdata.get('id','')
		sem_section = postdata.get('sem_section', '')
		subject_id = postdata.get('subject_id', '')
		day_name = postdata.get('day_name','')
		hour_no = postdata.get('hour_no','')
		slot_details = tt_record.objects.filter(tt_id = curr_id,date = date.today())
		slot_date = slot_details.values('date')
		print(slot_date)
	return render(request,'post_login\slot_confirm.html',{'id':curr_id, 'sem_section': sem_section,'subject_id':subject_id,'day_name': day_name,'hour_no':hour_no,'slot_details': slot_date})



@login_required(login_url='/accounts/login')
def slot_updated(request):
	if request.method == "POST":
		postdata = request.POST.copy()
		curr_id = postdata.get('id','')
		sem_section = postdata.get('sem_section', '')
		subject_id = postdata.get('subject_id', '')
		day_name = postdata.get('day_name','')
		hour_no = postdata.get('hour_no','')
		topic_discussed = postdata.get('topic','')
		description = postdata.get('description','')
		slot_date = postdata.get('slot_date','')
		slot_details = tt_record.objects.filter(tt_id = curr_id,date = date.today())
		slot_details.update(topic_discussed = topic_discussed,description = description)
	return render(request,'post_login\slot_updated.html')


@login_required(login_url='/accounts/login')
def resc_slot_update(request):
	if request.method == "POST":
		postdata = request.POST.copy()
		curr_date = postdata.get('date','')
		curr_id = postdata.get('id','')
		sem_section = postdata.get('sem_section', '')
		subject_id = postdata.get('subject_id', '')
		day_name = postdata.get('day_name','')
		hour_no = postdata.get('hour_no','')
		#slot_details = rescheduled_classes.objects.filter(tt_id = curr_id,date = date.today())
		#slot_date = slot_details.values('date')
		#print(slot_date)
	return render(request,'post_login\\resc_slot_update.html',{'date':curr_date,'id':curr_id, 'sem_section': sem_section,'subject_id':subject_id,'day_name': day_name,'hour_no':hour_no})

@login_required(login_url='/accounts/login')
def resc_slot_updated(request):
	if request.method == "POST":
		postdata = request.POST.copy()
		curr_date = postdata.get('date','')
		curr_id = postdata.get('id','')
		sem_section = postdata.get('sem_section', '')
		subject_id = postdata.get('subject_id', '')
		day_name = postdata.get('day_name','')
		hour_no = postdata.get('hour_no','')
		topic_discussed = postdata.get('topic','')
		description = postdata.get('description','')
		slot_date = postdata.get('slot_date','')
		resc_slot_details = rescheduled_classes.objects.filter(rescheduled_id = curr_id,resc_date = curr_date)
		resc_slot_details.update(resc_topic_discussed = topic_discussed,resc_description = description)
	return render(request,'post_login\\resc_slot_updated.html')