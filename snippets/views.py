from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

# creating a function-based view with the @api_view decorator, which will shorten up
# a lot of the code previously written with the JSONResponse object, this one will
# allow GET or POST req/res
@api_view(['GET', 'POST'])
# this function will pertain to the entire snippet list, vs singling one out which
# we will see below
def snippet_list(request, format=None):
    """
    List all snippets, or create a new snippet.
    """
    # if the request object is 'GET' then do the following:
    if request.method == 'GET':
        # set 'snippet' to all of the Snippet objects in the list
        snippets = Snippet.object.all()
        # set 'serializer' to one query set of snippet objects
        serilaizer = SnippetSerializer(snippets, many=True)
        # return this serialized data as 1 Response object that will take on the
        # content type requested by the client
        return Response(serilaizer.data)

    # if the request object is 'POST' then do the following:
    elif request.method == 'POST':
        # set 'serializer' to serialized request data
        serializer = SnippetSerializer(data=request.data)
        # if this serializer is valid, do the following:
        if serializer.is_valid():
            # save serialized request data
            serializer.save()
            # return a Response object of 1- serialized data that has now been
            # saved, 2- send an explicit status code of 201, CREATED
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # if the serializer is not valid 1- send back a serializer error,
        # 2- send explicit status code of 400, BAD REQUEST
        return Response(serializer.errors, status=status.HTPP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    """
    Retrieve, update, or delete a snippet instance.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    # else if the request object = 'PUT' do the following:
    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # else if the request object = 'DELETE' do the following:
    elif request.method == 'DELETE':
        # delete snippet
        snippet.delete()
        # return a Response object that has an explicit status of 204 NO CONTENT
        return Response(status=status.HTTP_204_NO_CONTENT)
