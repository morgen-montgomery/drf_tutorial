from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# create a class 'SnippetList' as an APIView
class SnippetList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    # when SnippetList has a function of get, it creates an instance that
    # takes a request, and does the following:
    def get(self, request, format=None):
        # retrieve all snippet objects, turn them into a list, and set that to 'snippets'
        snippets = Snippet.objects.all()
        # take this list of objects and return them as one serilaized query set
        serializer = SnippetSerializer(snippets, many=True)
        # return the serialized data as a drf Response object
        return Response(serializer.data)

    # when SnippetList has a function of post, it creates an instance that
    # takes a request, and dows the following:
    def post(self, request, format=None):
        # take the request object data and turn it into serialized data, set
        # this to 'serializer'
        serializer = SnippetSerializer(data=request.data)
        # is the serializer is valid, do the following:
        if serializer.is_valid():
            # save serializer
            serializer.save()
            # return serialized data along with a drf explicit status code 201 CREATED
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # if serializer is not valid, return serializer errors, and explicit status code
        # 400 BAD REQUEST
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
