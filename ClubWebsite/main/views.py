from django.shortcuts import render,redirect,get_object_or_404
from .models import Profile,Event
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.utils import timezone
import datetime

# Create your views here.

def home(request):
	return render(request,'login.html',{})

def index(request):
	return render(request,'addMember.html',{})


def login_view(request):
	if request.method == 'POST':
	    username = request.POST.get('username', None)
	    password = request.POST.get('password', None)
	    if username and password:
	        user = authenticate(username=username, password=password)
	        if user:
	        	if user.is_active:
	        		login(request, user)
	        return redirect('/')
	    else:
	    	return redirect('/')
	return redirect('/')


@login_required
def register(request):
	if not request.user.is_superuser:
		return HttpResponse('The user is not superuser')
	elif request.method == 'POST':
		username = request.POST.get('username', None)
		password = request.POST.get('password', None)
		email = request.POST.get('email', None)
		batch = request.POST.get('batch', None)
		user, created = User.objects.get_or_create(username=username, email=email)
		if created:
		    user.set_password(password) 
		    user.save()
		    user.profile.batch = batch
		    user.profile.save()
		    return redirect('/')
		else :
			return redirect('/home/')
@login_required
def create_event(request):
	if request.method == 'POST':
		title = request.POST.get('title', None)
		description = request.POST.get('description', None)
		rules = request.POST.get('rules', None)
		prerequistes = request.POST.get('prerequistes', None)
		fee = request.POST.get('fee', None)
		venue = request.POST.get('venue', None)
		start_time = request.POST.get('start_time', None)
		end_time = request.POST.get('end_time', None)
		start_date = request.POST.get('start_date', None)
		end_date = request.POST.get('end_date', None)
		user = request.user
		host = user.username
		event = Event.objects.create(title=title,end_date=end_date,start_date=start_date,end_time=end_time,start_time=start_time,description=description,rules=rules,prerequistes=prerequistes,venue=venue,fee=fee,host=host)
		event.save()
		return redirect('/')
	elif request.method == 'GET':
		return render(request,'addEvent.html',{})

def event_list_view(request):
	obj = Event.objects.all()
	past = []
	future = []
	for x in obj :
		if x.end_date <datetime.date.today():
			past.append(x)
		elif x.end_date ==datetime.date.today() and x.end_time < datetime.datetime.now().time():
			past.append(x)
		else :
			future.append(x)
	return render(request,'events.html',{'past':past,'future':future})

def event_detailview(request,pk):
	obj = get_object_or_404(Event,pk=pk)
	past =0
	if obj.start_date < datetime.date.today() or (obj.start_date == datetime.date.today() and obj.start_time <datetime.datetime.now().time() ) :
		past=1
	return render(request,'eventDetails.html',{'obj':obj,'past':past})
