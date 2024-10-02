import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    description = models.TextField(blank=True)
    subscription_id = models.UUIDField(default=uuid.uuid4, unique=True)
