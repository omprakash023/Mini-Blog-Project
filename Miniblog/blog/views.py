# django imports
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.models import User

# rest framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.decorators import permission_classes 
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny,IsAuthenticated

# rest framework auth token
from rest_framework.authtoken.models import Token


# folder  import

# Create your views here.

class Index(APIView):
    permission_classes = [AllowAny] 
    def get(self,request):
        return render(request,'index.html')



class HandleRegister(APIView):
    permission_classes = [AllowAny,]

    def get(self,request):
        return render(request,'signup.html')

    def post(self,request):
        data = request.POST
        print(data)
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('Cpassword')

        # Create User Name 
        user = User.objects.create_user(username,email,password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return Response(data={"user": username, 'success': 'Signup Successfully!'})
   

        
        # if :
        #     return render(request,'signup.html',{"success_msg": "Signup Successfully!" })
        # else:
        #     return render(request,'signup.html' ,{"data":serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)
            # return Response(template_name='login.html' ,data=serializer.errors, status=status.HTTP_401_UNAUTHORIZED)




class HandleLogin(APIView):
        
        permission_classes = [AllowAny,]

        def get(self,request):
            return render(request,'login.html')

        def post(self,request):
            username = request.data['username']
            password = request.data['password']
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    token, _ = Token.objects.get_or_create(user=user)
                    token.save()
                    login(request,user)
                    # return render(request,'index.html' ,{'success': "Logged In Successfully !"})
                    return redirect('index')
                    # return Response(template_name='index.html',data={"user": response_serializer.data, "token": token.key})
                else:
                    return render(request,'login.html' ,{'error': "Password is Incorrect"}, status=status.HTTP_401_UNAUTHORIZED)
                    # return Response(data={'password': 'Password is Incorrect'}, status=status.HTTP_401_UNAUTHORIZED)
            except:
                return render(request,'login.html' ,{'error': "User with this Username doesn't exist"}, status=status.HTTP_401_UNAUTHORIZED)

                


class HandleLogout(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self,request):
        logout(request)
        return redirect('index')