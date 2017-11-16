from django.shortcuts import render,redirect,get_object_or_404
from .models import Profile,Event,registration,feedback,project
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.utils import timezone
import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import feedbackSerializer,Event1Serializer,profileSerializer,EventSerializer,registrationSerializer
from rest_framework.generics import RetrieveAPIView,ListAPIView,CreateAPIView


# Create your views here.
class RegistrationAPIView(CreateAPIView):
	queryset = registration.objects.all()
	serializer_class = registrationSerializer

class FeedbackAPIView(CreateAPIView):
	queryset = feedback.objects.all()
	serializer_class = feedbackSerializer

@login_required
def eventregistrationsView(request,pk):
	if not request.user.is_superuser:
		return redirect('/profile/')
	event=get_object_or_404(Event,pk=pk)
	obj = registration.objects.filter(eventid=pk)
	return render(request,'eventregistrations.html',{'obj':obj,'event':event})

@login_required
def eventfeedbacksView(request,pk):
	if not request.user.is_superuser:
		return redirect('/profile/')
	event=get_object_or_404(Event,pk=pk)
	obj = feedback.objects.filter(eventid=pk)
	return render(request,'eventfeedbacks.html',{'obj':obj,'event':event})

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
		    return render(request,'addMember.html',{'msg':"success"})
		else :
			return render(request,'addMember.html',{'err':"User already Exist!!"})
	else:
		return render(request,'addMember.html',{})


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
		return render(request,'addEvent.html',{'msg':"success"})
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


def project_list_view(request):
	obj = project.objects.all()
	return render(request,'projects.html',{'obj':obj})

def event_list_view(request):
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
	return render(request,'events.html',{'past':past,'future':future})

def event_detailview(request,pk):
	obj = get_object_or_404(Event,pk=pk)
	past =0
	counts = registration.objects.filter(eventid=obj.id).count()
	if obj.end_date < datetime.date.today() or (obj.end_date == datetime.date.today() and obj.end_time <datetime.datetime.now().time() ) :
		past=1
	return render(request,'eventDetails.html',{'obj':obj,'past':past,'counts':counts})

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
		frameworks = request.POST.get('frameworks', None)
		bio = request.POST.get('bio', None)
		label = request.POST.get('label', None)
		location = request.POST.get('location', None)
		achivements = request.POST.get('achivements', None)
		company = request.POST.get('company', None)
		languages = request.POST.get('languages', None)
		he_profile = request.POST.get('he_profile', None)
		he_ques = request.POST.get('he_ques', None)
		spoj_ques = request.POST.get('spoj_ques', None)
		spoj_profile = request.POST.get('spoj_profile', None)
		git_repos = request.POST.get('git_repos', None)
		my_website = request.POST.get('my_website', None)

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
		user.profile.my_website = my_website
		user.profile.git_repos = git_repos
		user.profile.spoj_profile = spoj_profile
		user.profile.spoj_ques = spoj_ques
		user.profile.he_ques = he_ques
		user.profile.he_profile = he_profile
		user.profile.languages = languages
		user.profile.frameworks = frameworks
		user.profile.achivements = achivements
		user.profile.bio = bio
		user.profile.label = label
		user.profile.company = company
		user.profile.location = location
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
		frameworks = request.POST.get('frameworks', None)
		bio = request.POST.get('bio', None)
		label = request.POST.get('label', None)
		location = request.POST.get('location', None)
		achivements = request.POST.get('achivements', None)
		company = request.POST.get('company', None)
		languages = request.POST.get('languages', None)
		he_profile = request.POST.get('he_profile', None)
		he_ques = request.POST.get('he_ques', None)
		spoj_ques = request.POST.get('spoj_ques', None)
		spoj_profile = request.POST.get('spoj_profile', None)
		git_repos = request.POST.get('git_repos', None)
		my_website = request.POST.get('my_website', None)
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
		user.profile.my_website = my_website
		user.profile.git_repos = git_repos
		user.profile.spoj_profile = spoj_profile
		user.profile.spoj_ques = spoj_ques
		user.profile.he_ques = he_ques
		user.profile.he_profile = he_profile
		user.profile.languages = languages
		user.profile.frameworks = frameworks
		user.profile.achivements = achivements
		user.profile.bio = bio
		user.profile.label = label
		user.profile.company = company
		user.profile.location = location
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
		'bio':user.profile.bio,
		'label':user.profile.label,
		'location':user.profile.location,
		'he_profile':user.profile.he_profile,
		'company':user.profile.company,
		'spoj_profile':user.profile.spoj_profile,
		'he_ques':user.profile.he_ques,
		'spoj_ques':user.profile.spoj_ques,
		'git_repos':user.profile.git_repos,
		'my_website':user.profile.my_website,
		'languages':user.profile.languages,
		'frameworks':user.profile.frameworks,
		'achivements':user.profile.achivements,
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

@login_required
def add_project(request):
	if request.method == 'POST':
		title = request.POST.get('title', None)
		description = request.POST.get('description', None)
		owner = request.POST.get('owner', None)
		demo_link = request.POST.get('demo_link', None)
		source = request.POST.get('source', None)
		technologies = request.POST.get('technologies', None)
		proj = project.objects.create(title=title,description=description,demo_link=demo_link,source=source,technologies=technologies)
		proj.save()
		a=owner.split()
		for x in a:
			try:
				user=User.objects.get(username=x)
				proj.owner.add(user)
			except User.DoesNotExist:
				pass
		proj.save()
		return render(request,'addProject.html',{'msg':"success"})
	elif request.method == 'GET':
		return render(request,'addProject.html',{})