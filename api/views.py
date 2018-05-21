from api.models import Match
from api.permissions import IsOwnerOrReadOnly
from api.serializers import MatchSerializer
from api.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions

import chess

class MatchViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update`, and `destroy` action.
    """
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(white=self.request.user)

    def perform_update(self, serializer):
        # Check for move legality and then proceed
        serializer.save()

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
