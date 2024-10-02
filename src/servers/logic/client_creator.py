from django.db.transaction import atomic

from servers.models import Inbound, Client
from servers.xui_client.client import add_client
from users.models import User


class ClientCreator:
    def __init__(self, inbound: Inbound, user: User):
        self.inbound = inbound
        self.user = user

    @atomic
    def do(self):
        client_id, email = add_client(self.inbound)
        client = Client.objects.create(
            inbound=self.inbound,
            user=self.user,
            xui_id=client_id,
            enable=True,
            description=f"x_ui email: {email}",
        )

        return client
