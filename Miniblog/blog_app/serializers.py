# rest framework imports
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.fields import CurrentUserDefault

# djnago imports
from django.contrib.auth.models import User

# file imports
from .models import BlogModel

class formserializers(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())],required=True,max_length=32)
    password = serializers.CharField(min_length=6)

    def create(self,validate_data):
        user = User.objects.create_user(validate_data['username'],validate_data['email'],
            validate_data['password'])
        return user

    class Meta:
        model = User
        fields = ('id','email','username','password')


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogModel
        fields = ['title','content','created_at']