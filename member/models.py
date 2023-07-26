from django.db import models

# Create your models here.
class Member(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=200, unique=True)
    firstname = models.CharField(max_length=100, null=True, blank=True)
    lastname = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.username
