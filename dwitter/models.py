from django.db import models
from django.contrib.auth.models import User

class Dweet(models.Model):
    code = models.CharField(max_length=140)
    posted = models.DateTimeField()
    author = models.ForeignKey(User)
