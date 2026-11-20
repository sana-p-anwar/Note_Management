from django.db import models
from django.contrib.auth.models import User
class NotesDb(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return self.title
         

# Create your models here.
class TaskDb(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=50,default ="pending")
    created_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title