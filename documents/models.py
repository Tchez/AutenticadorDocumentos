from django.db import models
from users.models import CustomUser


class Document(models.Model):
    owner = models.ForeignKey(
        CustomUser, related_name="documents", on_delete=models.CASCADE
    )
    title = models.CharField("Título", max_length=255)
    content = models.TextField("Conteúdo")
    signature = models.TextField("Assinatura", null=True, blank=True)
    signed_hash = models.CharField(
        "Hash Assinado", max_length=64, null=True, blank=True
    )
