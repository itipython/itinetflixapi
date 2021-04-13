from rest_framework import serializers
from netflixdb.models import Actor

class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = ["name"]