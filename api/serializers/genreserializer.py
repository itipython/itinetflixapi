from rest_framework import serializers
from netflixdb.models import Genre

class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ["name"]
