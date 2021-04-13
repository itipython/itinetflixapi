from rest_framework import serializers
from netflixdb.models import Show
from .genreserializer import GenreSerializer
from .prizeserializer import PrizeSerializer
from .actorserializer import ActorSerializer
from .authorserializer import AuthorSerializer
from .producerserializer import ProducerSerializer
from .userreviewserializer import UserReviewSerializer

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