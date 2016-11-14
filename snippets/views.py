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


# this takes care of what I had for both UserList class and
# UserDetail class, which used the same queryset and
# serializer_class, with 'ListAPIView' and 'RetrieveAPIView'
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides 'list' and 'detail' actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

# create class 'SnippetList and pass in a generic that will create and list object,
# generate a generic API view
class SnippetList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# create class 'SnippetDetail' and pass in a generic that will retrieve, update and
# destroy a specific object, and generate a generic API view
class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })
