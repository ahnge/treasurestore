from typing import Any
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class CustomUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="custom_user")
    phone_number = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.user.username} - {self.phone_number}"


class NewsLetterSubcribers(models.Model):
    email = models.EmailField(max_length=128)

    def __str__(self):
        return f"{self.email}"
