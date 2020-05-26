from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from .models import Dweet, Comment
from .webhooks import Webhooks
from .notifications import notify_new_like, notify_new_comment, notify_new_dweet


@receiver(post_save, sender=Dweet, dispatch_uid="new_dweet_notifications_signal")
def new_dweet_notifications(sender, instance, created, **kwargs):
    if(created):
        Webhooks.new_dweet_notifications(instance)
        notify_new_dweet(instance)


@receiver(post_save, sender=Comment, dispatch_uid="new_comment_notifications_signal")
def new_comment_notifications(sender, instance, created, **kwargs):
    if(created):
        notify_new_comment(dweet=instance.reply_to, comment=instance)


@receiver(m2m_changed, sender=Dweet.likes.through, dispatch_uid="new_comment_notifications_signal")
def new_likes_notifications(sender, instance, action, reverse, model, pk_set, using, **kwargs):
    if(action == "post_add" and not reverse):
        notify_new_like(dweet=instance, new_likes=pk_set)
