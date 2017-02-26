from django.db import models
from django.contrib.auth.models import User


class Dweet(models.Model):
    code = models.TextField()
    posted = models.DateTimeField()
    reply_to = models.ForeignKey("self", on_delete=models.SET_NULL,
                                 null=True, blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="liked")
    hotness = models.FloatField(default=1.0)

    def __unicode__(self):
        return 'd/' + str(self.id) + ' (' + self.author.username + ')'

    class Meta:
        ordering = ('-posted',)


class Comment(models.Model):
    text = models.TextField()
    posted = models.DateTimeField()
    reply_to = models.ForeignKey(Dweet, on_delete=models.CASCADE,
                                 related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __unicode__(self):
        return ('c/' +
                str(self.id) +
                ' (' +
                self.author.username +
                ') to ' +
                str(self.reply_to))

    class Meta:
        ordering = ('-posted',)
