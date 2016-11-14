from django.contrib.auth.models import User

from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import UserSerializer
from rest_framework import permissions
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics

from rest_framework.decorators import api_view
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.reverse import reverse

from rest_framework import viewsets
from rest_framework.decorators import detail_route

# this takes care of what I had for both UserList class and
# UserDetail class, which used the same queryset and
# serializer_class, with 'ListAPIView' and 'RetrieveAPIView'
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides 'list' and 'detail' actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


# this replaces the need to use 'SnippetList', 'SnippetDetail', AND
# 'SnippetHighlight', as all of this functionality is now
# provided using ModelViewSet in the SnippetViewSet class
class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list', 'create', 'retrieve',
    'update', and 'destroy' actions.

    Additionally we also provide an extra 'highlight' action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = seld.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
