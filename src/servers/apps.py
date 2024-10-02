from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ServersConfig(AppConfig):
    name = "servers"
    verbose_name = _("Servers")

    def ready(self):
        from . import signal_handlers  # noqa
