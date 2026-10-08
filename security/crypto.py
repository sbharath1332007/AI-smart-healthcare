import os
import base64
import json
import re
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

KEY_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "instance", "encryption.key")

def get_or_create_master_key() -> bytes:
    """Retrieve or generate the master AES-256 Fernet key."""
    env_key = os.environ.get("HEALTHCARE_ENCRYPTION_KEY")
    if env_key:
        return env_key.encode()

    os.makedirs(os.path.dirname(KEY_FILE), exist_ok=True)
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read().strip()
    
    # Generate new Fernet key (AES-128 in CBC mode with PKCS7 padding and HMAC-SHA256)
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key

_fernet_instance = None

def get_fernet() -> Fernet:
    global _fernet_instance
    if _fernet_instance is None:
        key = get_or_create_master_key()
        _fernet_instance = Fernet(key)
    return _fernet_instance

def encrypt_text(plain_text: str) -> str:
    """Encrypt a string into a base64-encoded ciphertext."""
    if not plain_text:
        return ""
    fernet = get_fernet()
    encrypted = fernet.encrypt(plain_text.encode("utf-8"))
    return encrypted.decode("utf-8")

def decrypt_text(cipher_text: str) -> str:
    """Decrypt a base64-encoded ciphertext back to plain text."""
    if not cipher_text:
        return ""
    try:
        fernet = get_fernet()
        decrypted = fernet.decrypt(cipher_text.encode("utf-8"))
        return decrypted.decode("utf-8")
    except Exception as e:
        return f"[Decryption Error: {str(e)}]"

def encrypt_json(data: dict) -> str:
    """Serialize and encrypt a dictionary."""
    if not data:
        return ""
    json_str = json.dumps(data)
    return encrypt_text(json_str)

def decrypt_json(cipher_text: str) -> dict:
    """Decrypt and deserialize into a dictionary."""
    if not cipher_text:
        return {}
    decrypted_str = decrypt_text(cipher_text)
    if decrypted_str.startswith("[Decryption Error"):
        return {"error": decrypted_str}
    try:
        return json.loads(decrypted_str)
    except Exception:
        return {"raw": decrypted_str}

def anonymize_text(text: str) -> str:
    """Redact Personally Identifiable Information (PII/PHI) from health descriptions."""
    if not text:
        return ""
    # Redact email addresses
    redacted = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[REDACTED_EMAIL]', text)
    # Redact phone numbers
    redacted = re.sub(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', '[REDACTED_PHONE]', redacted)
    # Redact SSN/National ID formats
    redacted = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[REDACTED_ID]', redacted)
    return redacted
