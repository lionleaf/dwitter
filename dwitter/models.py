from django.db import models
from django.contrib.auth.models import User


class Dweet(models.Model):
    code = models.TextField()
    posted = models.DateTimeField()
    reply_to = models.ForeignKey("self", on_delete=models.SET_NULL,
                                 null=True, blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="liked")
    hotscore = models.IntegerField(default=1)

    class Meta:
        ordering = ('-posted',)


class Comment(models.Model):
    text = models.TextField()
    posted = models.DateTimeField()
    reply_to = models.ForeignKey(Dweet, on_delete=models.CASCADE,
                                 related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-posted',)
