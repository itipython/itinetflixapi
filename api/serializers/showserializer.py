from rest_framework import serializers
from netflixdb.models import Show
from .genreserializer import GenreSerializer
from .prizeserializer import PrizeSerializer
from .authorserializer import AuthorSerializer
from .actorserializer import ActorSerializer
from .producerserializer import ProducerSerializer

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
                    'prizes', 'authors', 'producers', 'actors', 'description']
