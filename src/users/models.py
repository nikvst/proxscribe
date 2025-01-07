import uuid

from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models

from app.utils.username_generator import generate_username


class UserManager(DjangoUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        xui_user_id = generate_username()
        extra_fields["xui_user_id"] = xui_user_id
        return super()._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    description = models.TextField(blank=True)
    subscription_id = models.UUIDField(default=uuid.uuid4, unique=True)
    xui_user_id = models.CharField(max_length=128, unique=True)

    objects = UserManager()
