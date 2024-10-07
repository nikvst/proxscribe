from urllib.parse import quote

from django.db import models


class Server(models.Model):
    name = models.CharField(max_length=255)
    api_url = models.URLField(max_length=2000)
    description = models.TextField(blank=True)

    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Inbound(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)

    xui_id = models.IntegerField(null=True, blank=True)
    remark = models.CharField(max_length=1024, blank=True)
    protocol = models.CharField(max_length=50)
    priority = models.IntegerField(default=1000)
    connection_url_template = models.CharField(max_length=4096, blank=True)
    description = models.TextField(blank=True)
    client_default_config = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.remark

    @property
    def unmanaged(self) -> bool:
        """
        If the xui_id field is not filled, then this is an unmanaged Inbound,
        meaning its settings should not be fetched from xiu server.
        """
        return not bool(self.xui_id)


class Client(models.Model):
    inbound = models.ForeignKey(Inbound, on_delete=models.CASCADE)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, null=True, related_name="clients"
    )

    email = models.CharField(max_length=1024, blank=True)
    enable = models.BooleanField(default=True)

    description = models.TextField(blank=True)
    settings = models.JSONField(default=dict, blank=True)

    @property
    def connection_url(self):
        return self.inbound.connection_url_template.format(
            connection_name=quote(self.inbound.remark), **self.settings
        )
