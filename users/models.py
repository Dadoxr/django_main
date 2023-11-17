from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name="контактный email", unique=True)
    confirmation_code = models.CharField(
        max_length=6, verbose_name="код подтверждения", blank=True, null=True
    )
    comment = models.TextField(verbose_name="комментарий", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    class Meta:
        verbose_name = "юзер"
        verbose_name_plural = "юзеры"
