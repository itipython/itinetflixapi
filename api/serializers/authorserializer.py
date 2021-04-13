from rest_framework import serializers
from netflixdb.models import Author

class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ["name"]