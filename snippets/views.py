from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import generics
from django.contrib.auth.models import User
from snippets.serializers import UserSerializer
from rest_framework import permissions
# typical method

"""
class JSONResponse(HttpResponse):

    def __init__(self,data,**kwargs):

        content=JSONRenderer().render(data)
        kwargs['content_type']='application/json'
        super(JSONResponse,self).__init__(content,**kwargs)
"""


#function based view
"""
@api_view(['GET','POST'])

def snippet_list(request,format=None):


    if request.method=='GET':
        snippets=Snippet.objects.all()
        serializer=SnippetSerializer(snippets,many=True)
        return Response(serializer.data)

    elif request.method=='POST':

       # data=JSONParser().parse(request)
        serializer=SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
def snippet_detail(request, pk,format=None):

        try:
            snippet = Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = SnippetSerializer(snippet)
            return Response(serializer.data)

        elif request.method == 'PUT':
           # data = JSONParser().parse(request)
            serializer = SnippetSerializer(snippet, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            snippet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
"""

#class based views

"""
class SnippetList(APIView):

    def get(self,request,format=None):

        snippets=Snippet.objects.all()
        serializer=SnippetSerializer(snippets,many=True)
        return Response(serializer.data)

    def post(self,request,format=None):

        serializer=SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):

    def get_object(self,pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self,request,pk,format=None):

        snippet=self.get_object(pk)
        serializer=SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self,request,pk,format=None):

        snippet=self.get_object(pk)
        serializer=SnippetSerializer(snippet,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk,format=None):

        snippet=self.get_objects(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""

#generic class based views

class SnippetList(generics.ListCreateAPIView):

    queryset=Snippet.objects.all()
    serializer_class=SnippetSerializer
    def perform_create(self, serializer):
     serializer.save(owner=self.request.user)
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Snippet.objects.all()
    serializer_class=SnippetSerializer
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,)

class UserList(generics.ListAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer