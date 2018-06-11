from api.models import Match, Player
from django.contrib.auth.models import User
from rest_framework import serializers

class MatchSerializer(serializers.HyperlinkedModelSerializer):
    white = serializers.ReadOnlyField(source='Player.objects.get(user=owner)',)

    class Meta:
        model = Match
        fields = ('id', 'url', 'created', 'white', 'black', 'pgn', 'difficulty',
                  'winner', 'detail')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Player
        fields = ('id', 'url', 'user', 'current', 'wins')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        player, created = Player.objects.update_or_create(user=user,
                              current=validated_data.pop('current'))
        return player
