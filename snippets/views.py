from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

# used when you want to grant access to users without a CSRF token
# (not a widely used practice)
@csrf_exempt
# creating a function for what the snippet list (ALL snippets) action will be
# look at the request object
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    # if object is 'GET', do the following:
    if request.method == 'GET':
        # retrieve all of the snippet objects (as a query set)
        snippets = Snippet.object.all()
        # serialize these snippet objects as 1 query set (this is why we use the many=True)
        serializer = SnippetSerializer(snippets, many=True)
        # return all of this as 1 HttpResponse in JSON form
        return JSONResponse(serilaizer.data)

    # if object is 'POST', do the following:
    elif request.method == 'POST':
        # parse the request object to turn it into Python native datatypes
        data = JSONParser().parse(request)
        # restore native datatypes into fully populated object instance
        serializer = SnippetSerializer(data=data)
        # if this passes all of the validators on the Snippet class
        if serializer.is_valid():
            # save the serialized object
            serializer.save()
            # return the response object in JSON and send a status code 201 for
            # request being fulfilled and resources have been successfully created
            return JSONResponse(serializer.data, status=201)
        # if request object is 'POST' and serializer is not valid, respond with an
        # error and status code 400 for server not processing request due to client error
        return JSONResponse(serializer.errors, status=400)


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
