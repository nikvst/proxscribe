from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from servers.models import Client
from users.models import User


class ClientInline(admin.TabularInline):
    model = Client
    autocomplete_fields = ("inbound",)
    extra = 0
    fields = ("inbound", "enable")
    show_change_link = True


@admin.register(User)
class UserAdmin(UserAdmin):
    inlines = (ClientInline,)

    fieldsets = (
        (None, {"fields": ("username", "password", "subscription_id")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "email", "description")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    readonly_fields = ("subscription_id",)


admin.site.unregister(Group)
