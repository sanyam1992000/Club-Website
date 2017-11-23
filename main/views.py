from django.shortcuts import render,redirect,get_object_or_404
from .models import Profile,Event,registration,feedback,project
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.utils import timezone
import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import projecthostSerializer,feedbackSerializer,Event1Serializer,profileSerializer,EventSerializer,registrationSerializer,UserSerializer
from rest_framework.generics import RetrieveAPIView,ListAPIView,CreateAPIView
import requests
import json

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


def contactus(request):

	return render(request,'contactus.html',{})

class ProjectHostAPIView(ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

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
	        	redirect('/profile/')
	        else:
	        	return render(request,'login.html',{'err':'Incorrect Username/Password!!'})
	    else:
	    	return render(request,'login.html',{'err':'Enter Username/Password correctly!!'})
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
		    url = 'http://2factor.in/API/V1/053efa22-e848-11e6-afa5-00163ef91450/ADDON_SERVICES/SEND/TSMS'
		    data = {'From': 'MANNAN','To':username,'TemplateName':'MANAN-welcome','VAR1':email,'VAR2':username,'VAR3':password}
		    headers = {'Content-Type': 'application/json'}
		    r = requests.post(url, data=json.dumps(data), headers=headers)
		    user.profile.batch = batch
		    user.profile.save()
		    return render(request,'addMember.html',{'msg':"success"})
		else :
			return render(request,'addMember.html',{'err':"User already Exist!!"})
	else:
		return render(request,'addMember.html',{})


@login_required
def create_event(request):
	obj = User.objects.all()
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
		return render(request,'addEvent.html',{'msg':"success",'obj':obj})
	elif request.method == 'GET':
		return render(request,'addEvent.html',{'obj':obj})

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
	for x in range(m1,m2-1,-1):
		member.append({'batch':x,'users':[]})

	print(member)
	print("-----")
	for x in obj:
		member[m1-x.profile.batch]['users'].append(x)
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
	live = []
	for x in obj :
		if x.end_date <datetime.date.today():
			past.append(x)
		elif x.end_date ==datetime.date.today() and x.end_time < datetime.datetime.now().time():
			past.append(x)
		elif x.start_date > datetime.date.today() or (x.start_date == datetime.date.today() and x.start_time > datetime.datetime.now().time()):
			future.append(x)
		else :
			live.append(x)
	return render(request,'events.html',{'past':past,'future':future,'live':live})

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
		location = request.POST.get('location', None)
		achivements = request.POST.get('achivements', None)
		company = request.POST.get('company', None)
		languages = request.POST.get('languages', None)
		he_profile = request.POST.get('he_profile', None)
		codechef_profile = request.POST.get('codechef_profile', None)
		spoj_profile = request.POST.get('spoj_profile', None)
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
		user.profile.spoj_profile = spoj_profile
		user.profile.codechef_profile = codechef_profile
		user.profile.he_profile = he_profile
		user.profile.languages = languages
		user.profile.frameworks = frameworks
		user.profile.achivements = achivements
		user.profile.bio = bio
		user.profile.company = company
		user.profile.location = location
		user.profile.save()
		return render(request,'myprofile.html',{'msg':"profile is saved",'obj':user})
	else :
		return render(request,'myprofile.html',{'obj':request.user})
@login_required
def edit_event(request):
	obj = User.objects.all()
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
			return render(request,'editEventDetailByadmin.html',{'obj':obj,'err':"Event id is not correct"})
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
		return render(request,'editEventDetailByadmin.html',{'obj':obj,'msg':"successfull updated!!"})
	elif request.method == 'GET':
		return render(request,'editEventDetailByadmin.html',{'obj':obj})




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
		spoj_profile = request.POST.get('spoj_profile', None)
		codechef_profile = request.POST.get('codechef_profile', None)
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
		user.profile.spoj_profile = spoj_profile
		user.profile.he_profile = he_profile
		user.profile.languages = languages
		user.profile.frameworks = frameworks
		user.profile.achivements = achivements
		user.profile.bio = bio
		user.profile.label = label
		user.profile.company = company
		user.profile.location = location
		user.profile.codechef_profile=codechef_profile
		user.profile.save()
		return render(request,'editMemberDetailsByAdmin.html',{'msg':"profile is saved",'obj':user})
	else :
		return render(request,'editMemberDetailsByAdmin.html',{})

class dp_APIview(APIView):
	def post(self,request,*args,**kwargs):
		username = request.data.get('username')
		dp = request.data.get('dp')
		try :
			user = User.objects.get(username=mobile)
		except User.DoesNotExist:
			content = {'please move along': 'nothing to see here'}
			return Response(content, status=status.HTTP_404_NOT_FOUND)
		user.profile.dp = dp
		user.profile.save()
		user.save()
		content = {'msg':'success'}
		return Response(content,status=status.HTTP_200_OK)


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
		'codechef_profile':user.profile.codechef_profile,
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
	achivements = user.profile.achivements
	if achivements !="":
		achivements=achivements.split("--")
	return render(request,'Memberdetail.html',{'member':user,'ach':achivements})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })

@login_required
def add_project(request):
	obj = User.objects.all()
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
		proj.owner.add(request.user)
		for x in a:
			try:
				user=User.objects.get(username=x)
				proj.owner.add(user)
			except User.DoesNotExist:
				pass
		proj.save()
		return render(request,'addProject.html',{'msg':"success",'obj':obj})
	elif request.method == 'GET':
		return render(request,'addProject.html',{'obj':obj})

@login_required
def myproject_deleteview(request,pk):
	proj =get_object_or_404(project,pk=pk)

	if request.user in proj.owner.all() or request.user.is_superuser:
		proj.delete()
	return redirect('/myprojects/')

@login_required
def myproject_editview(request,pk):
	proj =get_object_or_404(project,pk=pk)

	if request.user in proj.owner.all() or request.user.is_superuser:
		if request.method =='POST':
			title = request.POST.get('title', None)
			description = request.POST.get('description', None)
			owner = request.POST.get('owner', None)
			demo_link = request.POST.get('demo_link', None)
			source = request.POST.get('source', None)
			technologies = request.POST.get('technologies', None)
			a=owner.split()
			b=proj.owner.all()
			for x in b:
				proj.owner.remove(x)
			proj.owner.add(request.user)
			for x in a:
				try:
					user=User.objects.get(username=x)
					proj.owner.add(user)
				except User.DoesNotExist:
					pass
			proj.title=title
			proj.description=description
			proj.demo_link=demo_link
			proj.source=source
			proj.technologies=technologies
			proj.save()
			return render(request,'editproject.html',{'proj':proj,'msg':"success"})
		else:
			return render(request,'editproject.html',{'proj':proj})
	return redirect('/myprojects/')

@login_required
def myprojects_view(request):
	user = request.user
	projects = user.project_set.all()
	return render(request,'myproject.html',{'member':user,'projects':projects})
