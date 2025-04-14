from asgiref.sync import async_to_sync

from django.db.models.signals import post_save
from django.dispatch import receiver
from warehouse.users.models import User
from config.websocket import broadcast_message


@receiver(post_save, sender=User)
def send_new_user_notification(sender, instance, created, **kwargs):
    if created:
        message = f"Новый пользователь {instance.username} был создан!"
        async_to_sync(broadcast_message)(message)
