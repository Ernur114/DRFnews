from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class ClientManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class Client(AbstractUser):
    username = None  
    email = models.EmailField(unique=True, max_length=100)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = ClientManager()
    activation_code = models.CharField(max_length=64, blank=True, null=True)
    def __str__(self):
        return self.email
