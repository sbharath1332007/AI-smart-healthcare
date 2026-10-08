"""
AI Smart Healthcare - Encrypted Database Management
Provides AES-256 encrypted persistence for Protected Health Information (PHI).
"""

import os
import sqlite3
import datetime
from typing import Optional, List, Dict, Any
from security.crypto import encrypt_text, decrypt_text, encrypt_json, decrypt_json
from security.auth import hash_password, verify_password

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "instance", "healthcare.db")


def get_db_connection() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize SQLite database with encrypted schema."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        encrypted_full_name TEXT NOT NULL,
        encrypted_profile TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS health_consultations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        encrypted_symptoms TEXT NOT NULL,
        encrypted_diagnosis TEXT NOT NULL,
        encrypted_diet_plan TEXT NOT NULL,
        encrypted_lifestyle_plan TEXT NOT NULL,
        urgency_level TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()


def log_security_event(user_id: Optional[int], action: str):
    try:
        conn = get_db_connection()
        conn.execute("INSERT INTO audit_logs (user_id, action) VALUES (?, ?)", (user_id, action))
        conn.commit()
        conn.close()
    except Exception:
        pass


def register_user(username: str, password: str, full_name: str, profile_data: dict) -> tuple[bool, str]:
    """Register a new patient with hashed password and encrypted profile."""
    username = username.strip().lower()
    if not username or not password:
        return False, "Username and password are required."

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, "Username is already registered."

    pwd_hash = hash_password(password)
    enc_name = encrypt_text(full_name)
    enc_profile = encrypt_json(profile_data)

    cursor.execute(
        "INSERT INTO users (username, password_hash, encrypted_full_name, encrypted_profile) VALUES (?, ?, ?, ?)",
        (username, pwd_hash, enc_name, enc_profile)
    )
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()

    log_security_event(user_id, "USER_REGISTRATION_ENCRYPTED")
    return True, str(user_id)


def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticate patient and return user dict if credentials match."""
    username = username.strip().lower()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    if verify_password(row["password_hash"], password):
        log_security_event(row["id"], "USER_LOGIN_SUCCESS")
        profile = decrypt_json(row["encrypted_profile"])
        full_name = decrypt_text(row["encrypted_full_name"])
        return {
            "id": row["id"],
            "username": row["username"],
            "full_name": full_name,
            "profile": profile,
            "created_at": row["created_at"]
        }
    else:
        log_security_event(row["id"], "USER_LOGIN_FAILED_ATTEMPT")
        return None


def save_consultation(
    user_id: Optional[int],
    symptoms_text: str,
    diagnosis_data: dict,
    diet_data: dict,
    lifestyle_data: dict,
    urgency_level: str
) -> int:
    """Store encrypted consultation record."""
    enc_symptoms = encrypt_text(symptoms_text)
    enc_diag = encrypt_json(diagnosis_data)
    enc_diet = encrypt_json(diet_data)
    enc_life = encrypt_json(lifestyle_data)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO health_consultations 
        (user_id, encrypted_symptoms, encrypted_diagnosis, encrypted_diet_plan, encrypted_lifestyle_plan, urgency_level)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (user_id, enc_symptoms, enc_diag, enc_diet, enc_life, urgency_level)
    )
    rec_id = cursor.lastrowid
    conn.commit()
    conn.close()

    log_security_event(user_id, f"HEALTH_CONSULTATION_ENCRYPTED_ID_{rec_id}")
    return rec_id


def get_user_consultations(user_id: int) -> List[Dict[str, Any]]:
    """Retrieve and decrypt consultation history for authorized user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM health_consultations WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()

    records = []
    for r in rows:
        records.append({
            "id": r["id"],
            "symptoms": decrypt_text(r["encrypted_symptoms"]),
            "diagnosis": decrypt_json(r["encrypted_diagnosis"]),
            "diet": decrypt_json(r["encrypted_diet_plan"]),
            "lifestyle": decrypt_json(r["encrypted_lifestyle_plan"]),
            "urgency": r["urgency_level"],
            "created_at": r["created_at"]
        })

    log_security_event(user_id, "CONSULTATIONS_DECRYPTED_FOR_VIEW")
    return records


def wipe_user_health_data(user_id: int) -> bool:
    """Permanently delete all consultation records and profile data for user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM health_consultations WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

    log_security_event(user_id, "PATIENT_DATA_PERMANENTLY_PURGED_RIGHT_TO_BE_FORGOTTEN")
    return True


def get_recent_security_logs(user_id: Optional[int], limit: int = 10) -> List[Dict[str, Any]]:
    """Fetch security audit logs for the user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    if user_id:
        cursor.execute(
            "SELECT * FROM audit_logs WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
            (user_id, limit)
        )
    else:
        cursor.execute("SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]
