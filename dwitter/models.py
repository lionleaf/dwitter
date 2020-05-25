import re
from django.db import models
from django.utils.functional import cached_property
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save, m2m_changed
from math import log
from datetime import datetime

from .utils import length_of_code


def get_sentinel_user():
    users = get_user_model().objects
    return users.get_or_create(username='[deleted]', is_active=False)[0]


@receiver(pre_delete, sender=User)
def soft_delete_user_dweets(instance, **kwargs):
    for dweet in Dweet.objects.filter(author=instance):
        dweet.delete()


class NotDeletedDweetManager(models.Manager):
    def get_queryset(self):
        base_queryset = super(NotDeletedDweetManager, self).get_queryset()
        return base_queryset.filter(deleted=False)


class Dweet(models.Model):
    code = models.TextField()
    posted = models.DateTimeField(db_index=True)
    reply_to = models.ForeignKey("self", on_delete=models.DO_NOTHING,
                                 null=True, blank=True)

    likes = models.ManyToManyField(User, related_name="liked", blank=True)
    hotness = models.FloatField(default=1.0, db_index=True)
    deleted = models.BooleanField(default=False)

    author = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user),
                               null=True, blank=True)

    objects = NotDeletedDweetManager()
    with_deleted = models.Manager()

    class Meta:
        ordering = ('-posted',)

    def delete(self):
        self.deleted = True
        self.save()

    def save(self, *args, **kwargs):
        self.calculate_hotness((self.pk is None))
        super(Dweet, self).save(*args, **kwargs)

    @cached_property
    def top_comment(self):
        """
        Return the top comment. This is mainly a caching optimization to avoid queries
        """
        return self.comments.first()

    @cached_property
    def dweet_length(self):
        return length_of_code(self.code)

    @cached_property
    def has_sticky_comment(self):
        """
        True when first comment should be stickied (first comment author == dweet author)
        """
        if self.top_comment is None:
            return False
        return self.top_comment.author == self.author

    def __str__(self):
        return 'd/' + str(self.id) + ' (' + self.author.username + ')'

    def calculate_hotness(self, is_new):
        """
        Hotness is inspired by the Hackernews ranking algorithm
        Read more here:
        https://medium.com/hacking-and-gonzo/how-hacker-news-ranking-algorithm-works-1d9b0cf2c08d
        """
        def epoch_seconds(date):
            epoch = datetime(2015, 5, 5)  # arbitrary start date before Dwitter existed
            naive = date.replace(tzinfo=None)
            td = naive - epoch
            return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)

        likes = 1
        if not is_new:
            likes = max(self.likes.count(), 1)

        order = log(likes, 2)
        # 86400 seconds = 24 hours.
        # So for every log(2) likes on a dweet, its effective
        # "posted time" moves 24 forward
        # In other words, it takes log2(likes) * 24hrs before
        # a dweet with a single like beat yours
        self.hotness = round(order + epoch_seconds(self.posted)/86400, 7)


@receiver(m2m_changed, sender=Dweet.likes.through, dispatch_uid="recalculate_hotness")
def recalc_hotness(sender, instance, action, **kwargs):
    if action in ("post_add", "post_remove", "post_clear"):
        instance.save()  # Trigger save on m2m_change forces calculate_hotness again


class Comment(models.Model):
    text = models.TextField()
    posted = models.DateTimeField()
    reply_to = models.ForeignKey(Dweet, on_delete=models.CASCADE,
                                 related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('posted',)

    def __str__(self):
        return ('c/' +
                str(self.id) +
                ' (' +
                self.author.username +
                ') to ' +
                str(self.reply_to))


class Hashtag(models.Model):
    name = models.CharField(max_length=30, unique=True, db_index=True)
    dweets = models.ManyToManyField(Dweet, related_name="hashtag", blank=True)

    def __str__(self):
        return '#' + self.name


# Go through hashtags mentioned in the comment
# and add them to the parent dweet.
# Should be idempotent.
@receiver(post_save, sender=Comment, dispatch_uid="add_hashtags_from_comment")
def add_hashtags(sender, instance, **kwargs):
    hash_pattern = re.compile(r'#(?P<hashtag>[_a-zA-Z][_a-zA-Z\d]*)')
    for hashtag in re.findall(hash_pattern, instance.text):
        h = Hashtag.objects.get_or_create(name=hashtag.lower())[0]
        if not h.dweets.filter(id=instance.reply_to.id).exists():
            h.dweets.add(instance.reply_to)
