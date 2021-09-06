from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'


class UserRole(models.TextChoices):
    USER = USER
    MODERATOR = MODERATOR
    ADMIN = ADMIN


class ConfirmationCode(models.Model):

    email = models.EmailField(null=False, unique=True)
    confirmation_code = models.CharField(
        max_length=20,
        blank=True,
        editable=False,
        null=True,
        unique=True)


class CustomUser(AbstractUser):
    email = models.EmailField(
        null=False,
        unique=True)

    first_name = models.CharField(
        null=True,
        max_length=30)
    last_name = models.CharField(
        null=True,
        max_length=30)

    bio = models.TextField(
        null=True,
        max_length=3000)

    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER
    )

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR
