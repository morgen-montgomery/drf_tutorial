from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics

# create class 'SnippetList and pass in a generic that will create and list object,
# generate a generic API view
class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


# creats a class 'SnippetDetail' and pass in Retrieve, Update, Destroy, and Generic mixins
class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    # get all snippet objects as a list and set them to 'queryset'
    queryset = Snippet.objects.all()
    # serialize things
    serializer_class = SnippetSerializer

    # if get is called, get and return the snippet of serialized data
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    # if put is called, update the snippet of serialized data
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    # if delete is called, find and destroy the snippet of serialized data
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
