from rest_framework.serializers import ModelSerializer,CharField
from .models import Profile
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

