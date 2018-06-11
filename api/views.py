from api.models import Match, Player
from api.permissions import IsOwnerOrReadOnly
from api.serializers import MatchSerializer
from api.serializers import UserSerializer
from api.serializers import PlayerSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.exceptions import APIException
import chess
import chess.uci

class MatchViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `list`, `create`, `retrieve`, and `update` actions.
    """
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    http_method_names = ['get', 'post', 'put', 'head']
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        player = Player.objects.get(user=self.request.user)

        if player.current == None:
            serializer.save(white=player)
        else:
            raise APIException("Player currently in another match")

    def perform_update(self, serializer):
        player = self.request.user.player
        match = self.get_object
        data = self.request.data

        if match().winner != "":
            raise APIException("Game is over")

        if match().white != player or player.current != match():
            raise APIException("Player currently in another match")

        if 'forfeit' in data and data['forfeit']:
            player.forfeit()
            serializer.save(winner=match().winner)
        elif 'move' in data:
            uci = data['move']

            if player.move(uci) and match().bot_move():
                serializer.save(pgn=match().pgn, winner=match().winner)
            else:
                raise APIException("Illegal move")

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
