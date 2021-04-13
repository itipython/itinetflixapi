from rest_framework import serializers
from netflixdb.models import UserReview

class UserReviewSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user.username')
    avatar = serializers.ReadOnlyField(source='user.avatar')
    show = serializers.ReadOnlyField(source='show.id')
    showname = serializers.ReadOnlyField(source='show.name')

    class Meta:
        model = UserReview
        fields =  ['user', 'show', 'rating', 'review', 'showname','avatar']