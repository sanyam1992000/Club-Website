from django.shortcuts import render,redirect,get_object_or_404
from .models import Profile,Event
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.utils import timezone
import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import profileSerializer

# Create your views here.

def home(request):
	if request.user.is_authenticated :
		return redirect('/profile/')
	return render(request,'index.html',{})

@login_required
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
	return redirect('/profile/')


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

@login_required
def editprofileview(request):
	if request.method == 'POST':
		username = request.POST.get('mobile', None)
		email = request.POST.get('email', None)
		fname = request.POST.get('fname', None)
		lname = request.POST.get('lname', None)
		github = request.POST.get('github', None)
		facebook = request.POST.get('facebook', None)
		linkedin = request.POST.get('linkedin', None)
		twitter = request.POST.get('twitter', None)
		try:
			user=User.objects.get(username=username)
		except User.DoesNotExist :
			return render(request,'myprofile.html',{'err':"user does not exist!!"})
		user.profile.email = email
		user.profile.fname = fname
		user.profile.lname = lname
		user.profile.github = github
		user.profile.facebook = facebook
		user.profile.twitter = twitter
		user.profile.linkedin = linkedin
		user.profile.save()
		return render(request,'myprofile.html',{'msg':"profile is saved",'obj':user})
	else :
		return render(request,'myprofile.html',{'err':"Profile was not updated!",'obj':user})

class getprofile_apiview(APIView):
	serializer_class = profileSerializer
	def post(self,request,*args,**kwargs):
		mobile = request.data.get('username')
		try :
			user = User.objects.get(username=mobile)
		except User.DoesNotExist:
			content = {'please move along': 'nothing to see here'}
			return Response(content, status=status.HTTP_404_NOT_FOUND)
		data ={
		'username':mobile,
		'fname':user.profile.fname,
		'lname':user.profile.lname,
		'batch':user.profile.batch,
		'github':user.profile.github,
		'facebook':user.profile.facebook,
		'linkedin':user.profile.linkedin,
		'twitter':user.profile.twitter,
		'email':user.profile.email,
		}
		serializer = profileSerializer(data=data)
		if serializer.is_valid():
			return Response(serializer.data,status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required
def myprofileview(request):
	if request.method == 'GET':
		user = request.user
		return render(request,'myprofile.html',{'obj':user})

