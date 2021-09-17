# django Imports
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate

# rest framework Imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.parsers import JSONParser

# simple JWT Imports
from rest_framework_simplejwt.tokens import RefreshToken  

# file imports
from .models import BlogModel
from .serializers import BlogSerializer,formserializers


# Create your views here.

# Register User
class HandleRegister(APIView):
    def post(self,request):
        serializer=formserializers(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            if user:
               token = RefreshToken.for_user(user)
               user_data = serializer.data
               return Response(data={"username":user_data['username'],"token":str(token.access_token)},status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login User 
class HandleLogin(APIView):
    permission_classes = [AllowAny,]
    def post(self,request):
        username = request.data['username']
        password = request.data['password']
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                token = RefreshToken.for_user(user)
                response_serializer=formserializers(user)
                return Response(data={"username": username, "token":str(token.access_token) ,"success":"welcome,Login Successfully!"},status=status.HTTP_200_OK)
            else:
                return Response(data={'password': 'Password is Incorrect'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(data={'username': "User with this Username doesn't exist"},
            status=status.HTTP_401_UNAUTHORIZED)

# Logout User
class HandleLogout(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self,request):
        logout(request)
        return Response(data={"success":"Logged Out Successfully!"},status=status.HTTP_200_OK)
        


# show all blogs
class ShowAllBlogs(ListAPIView):
    permission_classes = [AllowAny,]
    queryset = BlogModel.objects.all()
    serializer_class = BlogSerializer

# User Blog  
class UserBlogs(APIView):
    permission_classes = [IsAuthenticated]
    
    # Get user blogs
    def get(self,request,blog_id=None):
        user =request.user
        if blog_id:
            try:
                blog = BlogModel.objects.get(id=blog_id,user=user)
                serializer=BlogSerializer(blog)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            except:
                return Response(data={'message': "Blog Not present!"})
        else:
            user =request.user
            userblog = BlogModel.objects.filter(user=user)
            serializer=BlogSerializer(userblog,many=True)
            return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    # Create User Blog
    def post(self,request):
        data = JSONParser().parse(request)
        title=data['title']
        content=data['content']
        user = request.user
        blog,create = BlogModel.objects.get_or_create(
            title = title,content=content,
            user = request.user)
        if create:
            return Response(data={"title":blog.title,"content":blog.content,"message":"Blog created!"})
        return Response(data={"title":blog.title,"content":blog.content,"message":"Blog alredy present!"})

    # Update User Blog
    def put(self,request):
        data=JSONParser().parse(request)
        id = data['id']
        title=data['title']
        content=data['content']
        user = request.user
        try:
            blog = BlogModel.objects.get(id=id,user=user)
        except:
            return Response({"message":"This Blog not found for this user!"})
        if blog:
            if title:
                    blog.title = title
            if content:
                blog.content = content
            blog.save()
            return Response(data={"title":blog.title,"content":blog.content,"updated_at":blog.updated_at,"message":"Blog updated Successfully!"})

    def delete(self,request,blog_id=None):
        try:
            BlogModel.objects.get(
                id=blog_id,
                user=request.user
            ).delete()
        except:
            return Response(data={"message":"Blog not found for this user!"})
        return Response({"message":"Blog deleted!"})


