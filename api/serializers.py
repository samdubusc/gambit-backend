from api.models import Match
from rest_framework import serializers
from django.contrib.auth.models import User

class MatchSerializer(serializers.HyperlinkedModelSerializer):
    white = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Match
        fields = ('id', 'url', 'created', 'white', 'board', 'turn', 'castling',
                  'enPassant', 'halfMove', 'fullMove', 'isOver', 'difficulty',
                  'message')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username')
