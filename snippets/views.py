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
def snippet_list(request):
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


@csrf_exempt
# creating a function for what an individual snippet action will be
# look at the request object, and the snippet's pk
def snippet_detail(request, pk):
    """
    Retrieve, update, or delete a code snippet.
    """
    # look for something particular:
    try:
        # find and retrieve the snippet object with a matching pk
        snippet = Snippet.objects.get(pk=pk)
    # if you cannot find the snippet with a matching pk, do the following:
    except Snippet.DoesNotExist:
        # return HttpResponse with a status code of 404 for server not finding the
        # thing you are searching for
        return HttpResponse(status=404)

    # if object is 'GET', do the following:
    if request.method == 'GET':
        # serialize the snippet
        serializer = SnippetSerializer(snippet)
        # return this as an HttpResponse in JSON form
        return JSONResponse(serializer.data)

    # if object is 'PUT', do the following:
    elif request.method == 'PUT':
        # parse the request object to turn it into Python native datatypes
        data = JSONParser().parser(request)
        # restore native datatypes into fully populated object instance
        serializer = SnippetSerializer(snippet, data=data)
        # if this passes all of the validators on teh Snippet class
        if serializer.is_valid():
            # save the serialized object
            serializer.save()
            # return the response object
            return JSONResponse(serializer.data)
        # if request object is 'PUT' and serializer is not valid, respond with an
        # error and status code roo for server not processing request due to client error
        return JSONResponse(serializer.errors, status=400)

    # if object is 'DELETE', do the following:
    elif request.method == 'DELETE':
        # delete the snippet
        snippet.delete()
        # return HttpReponse as status code 204 for server successfully fulfilling
        # request with no content to send in response payload body
        return HttpResponse(status=204)
