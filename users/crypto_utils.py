import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding


def _ensure_bytes(data) -> bytes:
    """
    Garante que o input seja bytes. Se for uma string, a converte para bytes.

    Args:
    - data (str/bytes): Dados que possivelmente precisam ser convertidos em bytes.

    Retorna:
    - bytes: Dados convertidos (ou originais) em bytes.
    """
    if isinstance(data, str):
        return data.encode("utf-8")
    return data


def generate_keypair() -> tuple:
    """
    Gera um par de chaves RSA e retorna como (private_key, public_key).

    Retorna:
    - tuple: Chave privada e chave pública.
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key


def generate_keypair_pem() -> tuple:
    """
    Gera um par de chaves RSA e retorna como (private_key_pem, public_key_pem).

    Retorna:
    - tuple: Chave privada e chave pública no formato PEM.
    """
    private_key, public_key = generate_keypair()
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_key_pem, public_key_pem


def load_public_key_from_pem(pem_str) -> rsa.RSAPublicKey:
    """
    Carrega uma chave pública RSA de uma string PEM.

    Args:
    - pem_str (str): String no formato PEM da chave pública.

    Retorna:
    - rsa.RSAPublicKey: Chave pública RSA.
    """
    pem_bytes = _ensure_bytes(pem_str)
    return serialization.load_pem_public_key(pem_bytes, backend=default_backend())


def load_private_key_from_pem(pem_str) -> rsa.RSAPrivateKey:
    """
    Carrega uma chave privada RSA de uma string PEM.

    Args:
    - pem_str (str): String no formato PEM da chave privada.

    Retorna:
    - rsa.RSAPrivateKey: Chave privada RSA.
    """
    pem_bytes = _ensure_bytes(pem_str)
    return serialization.load_pem_private_key(
        pem_bytes, password=None, backend=default_backend()
    )


def sign_message(message, private_key) -> bytes:
    """
    Assina uma mensagem usando uma chave privada RSA.

    Args:
    - message (str/bytes): Mensagem a ser assinada.
    - private_key: Chave privada RSA.

    Retorna:
    - bytes: Assinatura da mensagem.
    """
    message_bytes = _ensure_bytes(message)

    signature = private_key.sign(
        message_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256(),
    )
    return signature


def verify_signature(message, signature: bytes, public_key) -> bool:
    """
    Verifica a assinatura de uma mensagem usando uma chave pública RSA.

    Args:
    - message (str/bytes): Mensagem original.
    - signature (bytes): Assinatura a ser verificada.
    - public_key: Chave pública RSA.

    Retorna:
    - bool: True se a assinatura for válida, False caso contrário.
    """
    message_bytes = _ensure_bytes(message)

    try:
        public_key.verify(
            signature,
            message_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256(),
        )
        return True
    except:
        return False


def generate_hash(message) -> str:
    """
    Gera um hash SHA256 para a mensagem dada.

    Args:
    - message (str/bytes): Mensagem a ser hashed.

    Retorna:
    - str: Hash SHA256 da mensagem.
    """
    message_bytes = _ensure_bytes(message)
    sha256 = hashlib.sha256()
    sha256.update(message_bytes)
    return sha256.hexdigest()


def verify_integrity(original_message, received_hash: str) -> bool:
    """
    Verifica a integridade da mensagem comparando com o hash recebido.

    Args:
    - original_message (str/bytes): Mensagem original.
    - received_hash (str): Hash da mensagem recebida.

    Retorna:
    - bool: Verdadeiro se a integridade da mensagem for confirmada, falso caso contrário.
    """
    calculated_hash = generate_hash(original_message)
    return calculated_hash == received_hash
