from rest_framework import serializers
from netflixdb.models import Prize

class PrizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prize
        fields = ["name"]
