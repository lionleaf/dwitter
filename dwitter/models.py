from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_delete


def get_sentinel_user():
    users = get_user_model().objects
    return users.get_or_create(username='[deleted]', is_active=False)[0]


@receiver(pre_delete, sender=User)
def soft_delete_user_dweets(instance, **kwargs):
    for dweet in Dweet.objects.filter(_author=instance):
        dweet.delete()


class NotDeletedDweetManager(models.Manager):
    def get_queryset(self):
        base_queryset = super(NotDeletedDweetManager, self).get_queryset()
        return base_queryset.filter(deleted=False)


class Dweet(models.Model):
    code = models.TextField()
    posted = models.DateTimeField()
    reply_to = models.ForeignKey("self", on_delete=models.DO_NOTHING,
                                 null=True, blank=True)

    likes = models.ManyToManyField(User, related_name="liked")
    hotness = models.FloatField(default=1.0)
    deleted = models.BooleanField(default=False)

    _author = models.ForeignKey(User, on_delete=models.SET_NULL,
                                null=True, blank=True)

    @property
    def author(self):
        return self._author or get_sentinel_user()

    @author.setter
    def author(self, value):
        self._author = value

    objects = NotDeletedDweetManager()
    with_deleted = models.Manager()

    def delete(self):
        self.deleted = True
        self.save()

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
