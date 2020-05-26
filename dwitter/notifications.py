from dwitter.models import DweetNotification
from django.utils import timezone

""" These functions are called with signals from signals.py,
    but the notification creation logic is kept in this file
"""


def get_watchers(dweet, exclude=[]):
    """ For now, everyone who has interacted with a dweet is a watcher. """
    watchers = [dweet.author]
    for liker in dweet.likes.all():
        watchers.append(liker)
    for comment in dweet.comments.all():
        watchers.append(comment.author)

    return [x for x in watchers if x.id not in exclude] 


def notify(watchers, dweet, verb, actors):
    for watcher in watchers:
        # Check if there's already an unread notification
        notification = DweetNotification.objects.filter(
                        recipient=watcher, dweet=dweet, verb=verb, read=False).first()

        if notification:
            notification.timestamp = timezone.now()
        else:
            notification = DweetNotification(recipient=watcher,
                                             dweet=dweet,
                                             verb=verb)
            notification.save()

        notification.actors.add(*actors)
        notification.save()


def notify_new_like(dweet, new_likes):
    """ new_likes is an array of pk to users who liked it the dweet """

    # For new likes only notify the author
    if dweet.author.id in new_likes:
        if len(new_likes) == 1:
            return
        new_likes.remove(dweet.author.id)

    notify([dweet.author], dweet, 'like', new_likes)


def notify_new_comment(dweet, comment):
    watchers = get_watchers(dweet, exclude=[comment.author.id])
    notify(watchers, dweet, 'comment', [comment.author.id])


def notify_new_dweet(dweet):
    if dweet.reply_to:
        # Remix notification time!
        watchers = get_watchers(dweet.reply_to, exclude=[dweet.author.id])
        notify(watchers, dweet, 'remix', [dweet.author.id])
