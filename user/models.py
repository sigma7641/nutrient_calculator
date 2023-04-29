from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User,related_name='member', blank=True)
    description = models.TextField(max_length=400, null=True, blank=True)

    def __str__(self):
        return self.name
