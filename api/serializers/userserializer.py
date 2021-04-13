from rest_framework import serializers
from netflixdb.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'dob', 'first_name',
                 'last_name', 'gender', 'avatar', 'country', 'phone','currentShow']
        extra_kwargs = {
            'password':{'write_only':'True'}
        }