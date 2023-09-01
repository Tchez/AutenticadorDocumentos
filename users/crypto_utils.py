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


def save_key_to_pem(key, filename: str) -> None:
    """
    Salva uma chave (privada ou pública) em um arquivo .pem.

    Args:
    - key: Chave para ser salva.
    - filename (str): Nome do arquivo.
    """
    if isinstance(key, rsa.RSAPrivateKey):
        with open(filename, "wb") as key_file:
            key_file.write(
                key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )
    elif isinstance(key, rsa.RSAPublicKey):
        with open(filename, "wb") as key_file:
            key_file.write(
                key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )
            )


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


def encrypt_message(message, public_key) -> bytes:
    """
    Criptografa uma mensagem usando uma chave pública RSA.

    Args:
    - message (str/bytes): Mensagem para ser criptografada.
    - public_key: Chave pública RSA.

    Retorna:
    - bytes: Mensagem criptografada.
    """
    message_bytes = _ensure_bytes(message)

    ciphertext = public_key.encrypt(
        message_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return ciphertext


def decrypt_message(ciphertext: bytes, private_key) -> str:
    """
    Descriptografa uma mensagem usando uma chave privada RSA.

    Args:
    - ciphertext (bytes): Mensagem criptografada em bytes.
    - private_key: Chave privada RSA.

    Retorna:
    - str: Mensagem descriptografada.
    """
    plaintext_bytes = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return plaintext_bytes.decode("utf-8")


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
