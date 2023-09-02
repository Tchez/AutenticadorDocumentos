from django.db import models
from users.models import CustomUser
from users.crypto_utils import verify_signature, load_public_key_from_pem


class Document(models.Model):
    owner = models.ForeignKey(
        CustomUser, related_name="documents", on_delete=models.CASCADE
    )
    title = models.CharField("Título", max_length=255)
    content = models.TextField("Conteúdo")
    signature = models.BinaryField("Assinatura", null=True, blank=True)
    hash = models.CharField("Hash", max_length=64, null=True, blank=True)

    def __str__(self):
        return self.title

    def verify_signature(self):
        if self.signature is None or self.hash is None:
            return False
        concat = self.content + self.hash
        public_key = load_public_key_from_pem(self.owner.public_key)
        return verify_signature(concat, self.signature, public_key)
