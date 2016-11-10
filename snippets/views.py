from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import mixins
from rest_framework import generics

# create a class 'SnippetList' and pass in List, Create, and GenericAPIView mixins
class Snippetlist(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    # get all snippet objects as a list and set them to 'queryset'
    queryset = Snippet.objects.all()
    # serialize things
    serializer_class = SnippetSerializer

    # if get is called, get and return a list of serialized data
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

        # if post is called, create an item list object
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


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
