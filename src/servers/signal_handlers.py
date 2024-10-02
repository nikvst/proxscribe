from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from servers.models import Client
from servers.xui_client.client import add_client, delete_client


@receiver(pre_save, sender=Client)
def create_client_in_xui(sender, instance: Client, **kwargs: dict):
    if not instance.email and instance.inbound.unmanaged is False:
        client_id, email, settings = add_client(instance.inbound)
        instance.xui_id = client_id
        instance.description += f"x_ui email: {email}"
        instance.settings = settings


@receiver(pre_delete, sender=Client)
def delete_client_in_xui(sender, instance: Client, **kwargs: dict):
    if instance.email and instance.inbound.unmanaged is False:
        delete_client(instance)
