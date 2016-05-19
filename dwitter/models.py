from django.db import models
from django.contrib.auth.models import User

class Dweet(models.Model):
    code = models.CharField(max_length=140)
    posted = models.DateTimeField()
    reply_to = models.ForeignKey("self", null=True, blank=True)
    author = models.ForeignKey(User)
    likes = models.ManyToManyField(User, related_name="liked")

class Comment(models.Model):
    text = models.CharField(max_length=140)
    posted = models.DateTimeField()
    reply_to = models.ForeignKey(Dweet, related_name="comments")
    author = models.ForeignKey(User)
