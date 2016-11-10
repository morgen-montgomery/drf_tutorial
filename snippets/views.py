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


# create a class 'SnippetDetail' as an APIView
class SnippetDetail(APIView):
    """
    Retrieve, update, or delete a snippet instance.
    """
    # when SnippetDetail has a function of get_object, it creates an instance that
    # takes a pk, and does the following:
    def get_object(self, pk):
        try:
            # return a snippet object with a certain pk
            return Snippet.objects.get(pk=pk)
        # if snippet does not exist, return a 404 Http error
        except Snippet.DoesNotExist:
            raise Http404

    # when SnippetDetail has a function of get, it creates an instance that
    # takes a request object, and a pk, and does the following:
    def get(self, request, pk, format=None):
        # get an instance of an object with a certain pk and set it to 'snippet'
        snippet = self.get_object(pk)
        # serialize this snippet and set it to 'serializer'
        serializer = SnippetSerializer(snippet)
        # return this serialized data asa drf Response object
        return Response(serializer.data)

    # when SnippetDetail has a function of put, it creates an instance that
    # takes a request object, and a pk, and does the following:
    def put(self, request, pk, format=None):
        # get an instance of an object with a certain pk and set it to 'snippet'
        snippet = self.get_object(pk)
        # create a serialized isntance of data for the request object and set it to 'serializer'
        serializer = SnippetSerializer(snippet, data=request.data)
        # if serializer is valid, do the following:
        if serializer.is_valid():
            # save serializer
            serializer.save()
            # return serialized data as a drf Response object
            return Response(serializer.data)
        # if serializer is not valid, return serializer errors, and explicit status code
        # 400 BAD REQUEST
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # when SnippetDetail has a function of delete, it creates an instance that
    # takes a request object, and a pk, and does the following:
    def delete(self, request, pk, format=None):
        # get an instance of an object with a certain pk and set it to 'snippet'
        snippet = self.get_object(pk)
        # delete snippet
        snippet.delete()
        # return drf Response object with an Http status of 204 NO CONTENT
        return Response(status=status.HTTP_204_NO_CONTENT)
