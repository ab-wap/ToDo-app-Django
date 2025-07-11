from django.db import models

# Create your models here.
class Todos(models.Model):
    title = models.CharField(max_length=100)
    # description = models.TextField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
# class Categories(models.Model):
#     name = models.CharField(max_length=50)
#     todos = models.ManyToManyField(Todos, related_name='categories')

#     def __str__(self):
#         return self.name