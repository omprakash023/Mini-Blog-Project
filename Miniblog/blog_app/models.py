# django Imports
from django.db import models
from django.contrib.auth.models import User

# rest framework Imports
from froala_editor.fields import FroalaField

#  file Imports
from .helpers import *

# Create your models here.

class BlogModel(models.Model):
    
    title = models.CharField(max_length=1000)
    content = FroalaField()
    slug = models.SlugField(max_length=1000,null=True, blank=True)
    image = models.ImageField(upload_to='blog')
    user = models.ForeignKey(User, blank=True , null=True , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.title} created by {self.user.username}'

    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.title)
        super(BlogModel, self).save(*args, **kwargs)