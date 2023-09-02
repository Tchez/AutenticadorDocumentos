from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    private_key = models.BinaryField("Chave privada", blank=True, null=True)
    public_key = models.BinaryField("Chave pública", blank=True, null=True)
