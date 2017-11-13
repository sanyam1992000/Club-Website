from django.shortcuts import render,redirect,get_object_or_404
from .models import Profile,Event,registration
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.utils import timezone
import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import Event1Serializer,profileSerializer,EventSerializer,registrationSerializer
from rest_framework.generics import RetrieveAPIView,ListAPIView,CreateAPIView


# Create your views here.
class RegistrationAPIView(CreateAPIView):
	queryset = registration.objects.all()
	serializer_class = registrationSerializer

@login_required
def eventregistrationsView(request,pk):
	if not request.user.is_superuser:
		return redirect('/profile/')
	event=get_object_or_404(Event,pk=pk)
	obj = registration.objects.filter(eventid=pk)
	return render(request,'eventregistrations.html',{'obj':obj,'event':event})

def home(request):

	return render(request,'index.html',{})


class EventlistAPIView(ListAPIView):
	queryset = Event.objects.order_by('start_date','start_time')
	serializer_class = EventSerializer

class nearestEventsAPIView(ListAPIView):
	serializer_class = EventSerializer

	def get_queryset(self):
		obj = Event.objects.order_by('start_date','start_time')
		past = []
		future = []
		for x in obj :
			if x.end_date <datetime.date.today():
				past.append(x)
			elif x.end_date ==datetime.date.today() and x.end_time < datetime.datetime.now().time():
				past.append(x)
			else :
				future.append(x)
		future.sort(key = lambda x: (x.start_date , x.start_time))
		return future[:3]
		

@login_required
def index(request):
	if not request.user.is_superuser:
		return redirect('/profile/')
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
	        return redirect('/login/')
	    else:
	    	return redirect('/login/')
	elif request.method == 'GET':
		if request.user.is_authenticated :
			if request.user.is_superuser :
				return redirect('/home/')
			return redirect('/profile/')
		return render(request,'login.html',{})
	return redirect('/profile/')


@login_required
def register(request):
	if not request.user.is_superuser:
		return redirect('/profile/')
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
	if not request.user.is_superuser:
			return redirect('/profile/')
	elif request.method == 'POST':
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
		host = request.POST.get('host', None)
		event = Event.objects.create(title=title,end_date=end_date,start_date=start_date,end_time=end_time,start_time=start_time,description=description,rules=rules,prerequistes=prerequistes,venue=venue,fee=fee)
		event.save()
		a=host.split()
		for x in a:
			try:
				user=User.objects.get(username=x)
				event.host.add(user)
			except User.DoesNotExist:
				pass
		event.save()
		return redirect('/home/')
	elif request.method == 'GET':
		return render(request,'addEvent.html',{})

def member_list_view(request):
	obj = User.objects.all()
	m1=0
	m2=10000
	for x in obj:
		if x.profile.batch>m1:
			m1=x.profile.batch
		if x.profile.batch<m2:
			m2=x.profile.batch
	print(m1,m2)
	member = []
	for x in range(m2,m1+1):
		member.append({'batch':x,'users':[]})

	print(member)
	print("-----")
	for x in obj:
		member[x.profile.batch-m2]['users'].append(x)
	print(member)
	print("-----")
	return render(request,'members.html',{'member':member})


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
		return render(request,'myprofile.html',{'obj':request.user})
@login_required
def edit_event(request):
	if not request.user.is_superuser:
		return redirect('/profile/')
	elif request.method == 'POST':
		eventid = request.POST.get('eventid',None)
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
		host = request.POST.get('host', None)
		print(eventid)
		try:
			event=Event.objects.get(pk=eventid)
		except Event.DoesNotExist:
			return render(request,'editEventDetailByadmin.html',{'err':"Event id is not correct"})
		a=host.split()
		b=event.host.all()
		event.title=title
		event.description=description
		event.rules=rules
		event.fee=fee
		event.venue=venue
		event.start_time=start_time
		event.end_date=end_date
		event.end_time=end_time
		event.start_date = start_date
		for x in b:
			event.host.remove(x)
		for x in a:
			try:
				user=User.objects.get(username=x)
				event.host.add(user)
			except User.DoesNotExist:
				pass
		event.save()
		return render(request,'editEventDetailByadmin.html',{'msg':"successfull updated!!"})
	elif request.method == 'GET':
		return render(request,'editEventDetailByadmin.html',{})




@login_required
def editmemberprofileview(request):
	if not request.user.is_superuser:
		return redirect('/profile/')
	elif request.method == 'POST':
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
			return render(request,'editMemberDetailsByAdmin.html',{'err':"user does not exist!!"})
		user.profile.email = email
		user.profile.fname = fname
		user.profile.lname = lname
		user.profile.github = github
		user.profile.facebook = facebook
		user.profile.twitter = twitter
		user.profile.linkedin = linkedin
		user.profile.save()
		return render(request,'editMemberDetailsByAdmin.html',{'msg':"profile is saved",'obj':user})
	else :
		return render(request,'editMemberDetailsByAdmin.html',{})

class getprofile_apiview(APIView):
	serializer_class = profileSerializer
	def post(self,request,*args,**kwargs):
		mobile = request.data.get('username')
		print(mobile)
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

class getevent_apiview(APIView):
	serializer_class = Event1Serializer
	def post(self,request,*args,**kwargs):
		eventid = request.data.get('eventid')
		print(eventid)
		try :
			event = Event.objects.get(pk=eventid)
		except Event.DoesNotExist:
			content = {'please move along': 'nothing to see here'}
			return Response(content, status=status.HTTP_404_NOT_FOUND)
		host=""
		for x in event.host.all():
			host+=x.username+" "
		data ={
		'eventid':eventid,
		'host':host,
		'description':event.description,
		'title':event.title,
		'fee':event.fee,
		'rules':event.rules,
		'prerequistes':event.prerequistes,
		'venue':event.venue,
		'start_date':event.start_date,
		'end_date':event.end_date,
		'start_time':event.start_time,
		'end_time':event.end_time,
		}
		serializer = Event1Serializer(data=data)
		if serializer.is_valid():
			return Response(serializer.data,status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def memberprofileview(request,username):
	user = get_object_or_404(User,username=username)
	return render(request,'Memberdetail.html',{'user':user})