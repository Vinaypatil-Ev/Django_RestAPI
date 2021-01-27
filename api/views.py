#models
from django.db.models import query
from api.models import Blog
from api.serializers import BlogSerializers

#Http response
from django.http.response import Http404, JsonResponse
from django.shortcuts import HttpResponse

#rest framework
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins, generics

# Create your views here

# simplest example of rest 
# fuction based views(API)

@csrf_exempt
def show_data(request):
    if request.method == "GET":
        data = Blog.objects.all()
        seri = BlogSerializers(data, many=True)
        return JsonResponse(seri.data, safe=False)
    elif request.method == "POST":
        data =  JSONParser().parse(request)
        seri = BlogSerializers(data=data)
        if seri.is_valid():
            seri.save()
            return JsonResponse(seri.data, status=status.HTTP_201_CREATED)
        return JsonResponse(seri.errors, stauts=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def show_details(request, pk):
    try:
        blog = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        return HttpResponse(f"INVALID ID: {pk}", status=204)
    
    if request.method == "GET":
        seri = BlogSerializers(blog)
        return JsonResponse(seri.data)
    elif request.method == "PUT":
        data = JSONParser().Parse(request)
        seri = BlogSerializers(Blog, data=data)
        if seri.is_valid():
            seri.save()
            return HttpResponse(seri.data, status=201)
        return Http404()
    elif request.method == "DELETE":
        blog.delete()
        return HttpResponse(status=200)

# browasble api
@api_view(["GET", "POST"])
def browsable_data(request):
    if request.method == "GET":
        data = Blog.objects.all()
        seri = BlogSerializers(data, many=True)
        return Response(seri.data)
    elif request.method == "POST":
        seri = BlogSerializers(data=request.data)
        if seri.is_valid():
            seri.save()
            return Response(seri.data, status=status.HTTP_201_CREATED)
        return Response(seri.error, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(["GET", "PUT", "DELETE"])
def browsable_details(request, pk):
    try:
        blog = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        Response(f"INVALID ID: {pk}", status=status.status.HTTP_204_NO_CONTENT)
        
    if request.method == "GET":
        seri = BlogSerializers(blog)
        return Response(seri.data)
    elif request.method == "PUT":
        seri = BlogSerializers(Blog, request.data)
        if seri.is_valid():
            seri.save()
            return Response(f"DATA UPDATED: {seri.data}", status=status.status.HTTP_202_ACCEPTED)
        return Response(f"UPDATE FAILED", status=status.status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        blog.delete()
        return Response("Data Successfully deleted", status=status.status.HTTP_200_OK)
        
## Class Based views(API)

class ClassBasedApiShow(APIView):
    def get(self, request, format=None):
        data = Blog.objects.all()
        seri = BlogSerializers(data, many=True)
        return Response(seri.data)
    
    def post(self, request, format=None):
        data = BlogSerializers(data=request.data)
        if data.is_valid():
            data.save()
            return Response(f"ADDED SUCESSFULLY: {data.data}", status=status.HTTP_201_CREATED)
        return Response("FAILED TO CREATE", status=status.HTTP_400_BAD_REQUEST)
        

class ClassBasedApiDetails(APIView):
    def get_object(self, pk):
        try:
            return Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return Response("ERROR", status=status.HTTP_400_BAD_REQUEST)
   
    def get(self, request, pk):
        data = self.get_object(pk)
        seri = BlogSerializers(data)
        return Response(seri.data)
    
    def put(self, request, pk):
        data = self.get_object(pk)
        seri = BlogSerializers(data, data=request.data)
        if seri.is_valid():
            seri.save()
            return Response(f"UPDATE SUCESSFULLY: {seri.data}", status=status.HTTP_202_ACCEPTED)
        return Response(f"ERROR: key{pk}", status=status.HTTP_204_NO_CONTENT)
    
    def delete(self, request, pk):
        try:
            data = self.get_object(pk)
        except Blog.DoesNotExist:
            return Response(f"Invalid Key: {pk}", status=status.HTTP_400_BAD_REQUEST)
        data.delete()
        return Response(f"Content Deleted key:{pk}", status=status.HTTP_202_ACCEPTED)
    
## Using mixing to create api

class MixinShowApi(generics.CreateAPIView,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializers
    
    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)
    
class MixinShowDetails(generics.CreateAPIView,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       ):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializers
    
    def get(self, request, pk):
        return self.retrieve(request, id=pk)
    
    def put(self, request, pk):
        return self.update(request, id=pk)
    
    def delete(self, request, pk):
        return self.destroy(request, id=pk)
    
# GenericClassBasedView

class GenericClassShowApi(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializers
    
class GenericClassShowDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializers
    