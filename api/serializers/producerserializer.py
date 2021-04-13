from rest_framework import serializers
from netflixdb.models import Producer

class ProducerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producer
        fields = ["name"]