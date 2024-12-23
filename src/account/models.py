from django.db import models
from user.models import User
import uuid


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return f'Account for user: {self.user.email}'
