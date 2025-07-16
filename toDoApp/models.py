from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
# class Categories(models.Model):
#     name = models.CharField(max_length=50)
#     todos = models.ManyToManyField(Todos, related_name='categories')

#     def __str__(self):
#         return self.name