import hashlib
import os
import secrets
from functools import wraps
from flask import session, redirect, url_for, flash

def hash_password(password: str) -> str:
    """Hash password using PBKDF2-HMAC-SHA256 with a unique random salt."""
    salt = secrets.token_hex(16)
    kdf = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        iterations=100000
    )
    return f"{salt}:{kdf.hex()}"

def verify_password(stored_hash: str, provided_password: str) -> bool:
    """Verify provided password against the stored salt:hash string."""
    try:
        salt, expected_hash = stored_hash.split(":", 1)
        kdf = hashlib.pbkdf2_hmac(
            'sha256',
            provided_password.encode('utf-8'),
            salt.encode('utf-8'),
            iterations=100000
        )
        return secrets.compare_digest(kdf.hex(), expected_hash)
    except Exception:
        return False

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please sign in to access your secure health portal.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function
