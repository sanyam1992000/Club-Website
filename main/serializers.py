from rest_framework.serializers import ModelSerializer,CharField,IntegerField
from .models import Profile,Event,registration
from django.contrib.auth.models import User

class profileSerializer(ModelSerializer):
	username = CharField(max_length=100)
	class Meta :
		model = Profile 
		fields = [
		'username',
		'fname',
		'lname',
		'batch',
		'github',
		'facebook',
		'linkedin',
		'twitter',
		'email',
		'bio',
		'label',
		'location',
		'he_profile',
		'company',
		'spoj_profile',
		'he_ques',
		'spoj_ques',
		'git_repos',
		'my_website',
		'languages',
		'frameworks',
		'achivements',
		]

class hostSerializer(ModelSerializer):
	class Meta :
		model = Profile
		fields = [
		'fname',
		'lname',
		]


class UserSerializer(ModelSerializer):
	profile = hostSerializer(read_only=True)
	class Meta :
		model = User
		fields = [
		'username',
		'profile',
		]
class Event1Serializer(ModelSerializer):
	host = CharField(max_length=1000)
	eventid = IntegerField()
	class Meta :
		model = Event
		fields = [
		'eventid',
		'host',
		'description',
		'title',
		'fee',
		'rules',
		'prerequistes',
		'venue',
		'start_date',
		'end_date',
		'start_time',
		'end_time',
		]


class EventSerializer(ModelSerializer):
	host = UserSerializer(many=True ,read_only=True)
	class Meta :
		model = Event
		fields = [
		'pk',
		'host',
		'description',
		'title',
		'fee',
		'rules',
		'prerequistes',
		'venue',
		'start_date',
		'end_date',
		'start_time',
		'end_time',
		]

class registrationSerializer(ModelSerializer):
	class Meta :
		model =registration
		fields = [
		'eventid',
		'mobile',
		'email',
		'fname',
		'lname',
		'query',
		'College',
		]