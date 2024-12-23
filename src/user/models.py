from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    email = models.EmailField()
    uuid = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return f'User: {self.email}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['email'],
                name='Email constraint'
            ),
            models.UniqueConstraint(
                fields=['username'],
                name='Username constraint'
            ),
            models.UniqueConstraint(
                fields=['uuid'],
                name='UUID constraint'
            )
        ]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} profile'
