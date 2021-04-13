from rest_framework import serializers
from netflixdb.models import User
from .showhistoryserializer import ShowHistorySerializer
from .showplaylistserializer import ShowPlaylistSerializer
from .membershipserializer import MembershipSerializer

class UserFullSerializer(serializers.ModelSerializer):
    showsHistory = ShowHistorySerializer(source='showhistory_set', many=True)
    showsplaylist = ShowPlaylistSerializer(source='showplaylist_set', many=True)
    membership = MembershipSerializer()
    

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'dob', 'first_name',
                 'last_name', 'gender', 'avatar', 'country', 'phone'
                  ,'currentShow', 'showsHistory', 'showsplaylist', 'membership'
                  , 'membershipStartDate', 'isVerified', 'isPaid', 'age', 'isMembershipEnded']
        extra_kwargs = {
            'password':{'write_only':'True'},
            'membership' : {'read_only':'True'},
            'membershipStartDate':{'read_only':'True'},
            'isVerified':{'read_only':'True'},
             'isPaid':{'read_only':'True'}
        }

 