from django.db.models.signals import post_save
from django.dispatch import receiver
from warehouse.users.models import User
from config.websocket import broadcast_message


@receiver(post_save, sender=User)
def send_new_user_notification(sender, instance, created, **kwargs):
    if created:
        message = f"Новый пользователь {instance.username} был создан!"
        import asyncio
        asyncio.create_task(broadcast_message(message))
