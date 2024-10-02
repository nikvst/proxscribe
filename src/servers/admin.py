from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy

from servers.logic.import_inbounds import ServerConfigImporter
from servers.models import Server, Inbound, Client


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "api_url")

    actions = ["import_inbounds"]

    @admin.action(description=gettext_lazy("Import all inbounds"))
    def import_inbounds(self, request, queryset):
        inbounds_count = 0
        clients_count = 0
        clients_deleted_count = 0

        for server in queryset:
            counters = ServerConfigImporter(server).do()

            inbounds_count += counters["inbounds_count"]
            clients_count += counters["clients_count"]
            clients_deleted_count += counters["clients_deleted_count"]

        self.message_user(
            request,
            mark_safe(
                gettext_lazy(
                    f"{inbounds_count} inbounds were imported successfully."
                    f"<br>{clients_count} clients were imported successfully."
                    f"<br>{clients_deleted_count} clients were deleted."
                )
            ),
            level="success",
        )


@admin.register(Inbound)
class InboundAdmin(admin.ModelAdmin):
    list_display = ("id", "server", "remark", "priority", "unmanaged")
    search_fields = ("remark",)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "inbound", "user", "enable", "description")
    autocomplete_fields = ("user",)
