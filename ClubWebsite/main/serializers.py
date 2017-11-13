from rest_framework.serializers import ModelSerializer,CharField
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
		]

class UserSerializer(ModelSerializer):
	class Meta :
		model = User
		fields = [
		'username',
		]


class EventSerializer(ModelSerializer):
	host = UserSerializer(many=True ,read_only=True)
	class Meta :
		model = Event
		fields = [
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
		'Fullname',
		'College',
		]