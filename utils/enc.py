from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
import os

def _derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encode(data: str, password: str) -> str:
    salt = os.urandom(16)
    key = _derive_key(password, salt)
    f = Fernet(key)
    token = f.encrypt(data.encode())
    # Return salt + token, both base64 encoded
    return base64.urlsafe_b64encode(salt + token).decode()

def decode(encoded: str, password: str) -> str:
    raw = base64.urlsafe_b64decode(encoded.encode())
    salt = raw[:16]
    token = raw[16:]
    key = _derive_key(password, salt)
    f = Fernet(key)
    return f.decrypt(token).decode()
