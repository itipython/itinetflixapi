from rest_framework import serializers
from netflixdb.models import *



class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ["name"]


class ProducerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producer
        fields = ["name"]

class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ["name"]

class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = ["name"]

class PrizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prize
        fields = ["name"]



class ShowSerializer(serializers.ModelSerializer):

    genres = GenreSerializer(many=True)
    prizes = PrizeSerializer(many=True)
    authors = AuthorSerializer(many=True)
    producers = ProducerSerializer(many=True)
    actors = ActorSerializer(many=True)

    class Meta:
        model = Show
        fields = ['id','name', 'productionDate', 'rate', 'parentGuide',
                     'posterURL', 'language', 'country', 'genres',
                    'prizes', 'authors', 'producers', 'actors']



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'dob', 'first_name',
                 'last_name', 'gender', 'avatar', 'country', 'phone']
        extra_kwargs = {
            'password':{'write_only':'True'}
        }

class UserReviewSerializer(serializers.ModelSerializer):

    username = serializers.ReadOnlyField(source='user.username')
    avatar = serializers.ReadOnlyField(source='user.avatar')
    showname = serializers.ReadOnlyField(source='show.name')

    class Meta:
        model = UserReview
        fields =  ['user', 'show', 'avatar', 'rating', 'review', 'username','showname']


class ShowFullSerializer(serializers.ModelSerializer):

    genres = GenreSerializer(many=True)
    prizes = PrizeSerializer(many=True)
    authors = AuthorSerializer(many=True)
    producers = ProducerSerializer(many=True)
    actors = ActorSerializer(many=True)
    userReviews = UserReviewSerializer(source='userreview_set',many=True)

    class Meta:
        model = Show
        fields = '__all__'

class ShowHistroySerializer(serializers.ModelSerializer):
    showposter = serializers.ReadOnlyField(source='show.posterURL')
    showname = serializers.ReadOnlyField(source='show.name')

    class Meta:
        model = ShowHistory
        exclude = ['id']

class ShowPlaylistSerializer(serializers.ModelSerializer):
    showposter = serializers.ReadOnlyField(source='show.posterURL')
    showname = serializers.ReadOnlyField(source='show.name')

    class Meta:
        model = ShowPlaylist
        exclude = ['id']

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = "__all__"


class UserFullSerializer(serializers.ModelSerializer):
    showsHistory = ShowHistroySerializer(source='showhistory_set', many=True)
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

 