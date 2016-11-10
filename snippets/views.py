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



@api_view(['GET', 'PUT', 'DELETE'])
# create a function-based view for a specific snippet detail taking
# a request object with a pk as arguements
def snippet_detail(request, pk, format=None):
    """
    Retrieve, update, or delete a snippet instance.
    """
    try:
        # look for a snippet object with a certain pk
        snippet = Snippet.objects.get(pk=pk)
    # if snippet does not exist, do the following:
    except Snippet.DoesNotExist:
        # return a drf Response object with an explicit status 404 NOT FOUND
        return Response(status=status.HTTP_404_NOT_FOUND)

    # if request object = 'GET', do the following:
    if request.method == 'GET':
        # serialize snippet and ser it to 'serializer'
        serializer = SnippetSerializer(snippet)
        # return the serialized data as a drf Response object
        return Response(serializer.data)

    # else if the request object = 'PUT' do the following:
    elif request.method == 'PUT':
        # set 'serializer' to a serialized request object of the data
        serializer = SnippetSerializer(snippet, data=request.data)
        # if the serializer is valid, do the following:
        if serializer.is_valid():
            # save serilaizer
            serializer.save()
            # return a Response object of the serialized data
            return Response(serializer.data)
        # if serializer is not valid, return a Response object with a serliazer
        # error and an explicit status code of 400 BAD REQUEST
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # else if the request object = 'DELETE' do the following:
    elif request.method == 'DELETE':
        # delete snippet
        snippet.delete()
        # return a Response object that has an explicit status of 204 NO CONTENT
        return Response(status=status.HTTP_204_NO_CONTENT)
