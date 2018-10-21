from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Dweet
from .webhooks import Webhooks


@receiver(post_save, sender=Dweet, dispatch_uid="new_dweet_notifications_signal")
def new_dweet_notifications(sender, instance, created, **kwargs):
    if(created):
        Webhooks.new_dweet_notifications(instance)
