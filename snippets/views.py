from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics

# create class 'SnippetList and pass in a generic that will create and list object,
# generate a generic API view
class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


# create class 'SnippetDetail' and pass in a generic that will retrieve, update and
# destroy a specific object, and generate a generic API view
class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippets.objects.all()
    serializer_class = SnippetSerializer
