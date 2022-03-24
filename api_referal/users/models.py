from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = [
        "username",
    ]

    phone_number = models.CharField(
        max_length=15,
        unique=True,
        null=False,
        blank=False)
    invite_code = models.CharField(max_length=6, blank=False)
    confirmation_code = models.CharField(max_length=4)
    is_active = models.BooleanField(
        default=False,
    )

    class Meta:
        app_label = "users"
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["-id"]


class InputInviteCode(models.Model):
    my_code = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="my_code")
    foreign_code = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="foreign_code"
    )

    class Meta:
        unique_together = ("my_code", "foreign_code")
