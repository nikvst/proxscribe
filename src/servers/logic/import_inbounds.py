from servers.models import Server, Inbound, Client
from servers.xui_client.client import get_inbounds
from servers.xui_client.schemas.get_inbounds import (
    InboundSchema,
    VLESSSettingsClientSchema,
    SSSettingsClientSchema,
)


class ServerConfigImporter:
    def __init__(self, server: Server):
        self.server = server

    def do(self):
        clients_count = 0
        clients_deleted_count = 0

        inbounds_data = get_inbounds(self.server)
        inbounds_count = len(inbounds_data)

        for inbound_data in inbounds_data:
            inbound = self._update_or_create_inbound(inbound_data)

            clients_data = inbound_data.settings.clients

            clients_count += len(clients_data)
            self._sync_clients(inbound, clients_data)
            clients_deleted_count += self._delete_clients(inbound, clients_data)

        return {
            "inbounds_count": inbounds_count,
            "clients_count": clients_count,
            "clients_deleted_count": clients_deleted_count,
        }

    def _update_or_create_inbound(self, inbound_data: InboundSchema):
        inbound, _ = Inbound.objects.update_or_create(
            server=self.server,
            xui_id=inbound_data.id,
            defaults={
                "remark": inbound_data.remark,
                "protocol": inbound_data.protocol,
            },
        )
        return inbound

    def _sync_clients(
        self,
        inbound: Inbound,
        clients_data: list[VLESSSettingsClientSchema | SSSettingsClientSchema],
    ):
        for client_data in clients_data:
            Client.objects.update_or_create(
                inbound=inbound,
                email=client_data.email,
                defaults={
                    "description": f"x_ui email: {client_data.email}",
                    "enable": client_data.enable,
                    "settings": client_data.model_dump(),
                },
            )

    def _delete_clients(
        self,
        inbound: Inbound,
        clients_data: list[VLESSSettingsClientSchema | SSSettingsClientSchema],
    ):
        clients_deleted, _ = (
            Client.objects.filter(inbound=inbound)
            .exclude(email__in=[client_data.email for client_data in clients_data])
            .delete()
        )
        return clients_deleted
