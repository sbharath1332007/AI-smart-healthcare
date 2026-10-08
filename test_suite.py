"""
AI Smart Healthcare - Test Suite
Covers Cryptography, PBKDF2 Authentication, Diagnostic Engine, Diet/Lifestyle Protocols,
Emergency Red-Flag Triage, and REST API Endpoints.
"""

import unittest
import os
import tempfile
import json

from security.crypto import encrypt_text, decrypt_text, encrypt_json, decrypt_json, anonymize_text
from security.auth import hash_password, verify_password
from database.db import (
    init_db, register_user, authenticate_user, save_consultation,
    get_user_consultations, wipe_user_health_data, get_recent_security_logs
)
from engine.ai_analyzer import analyze_health_problem, detect_emergency_red_flags
from app import app


class TestAISmartHealthcare(unittest.TestCase):

    def setUp(self):
        init_db()
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_01_crypto_encryption_decryption(self):
        """Test AES-256 Fernet encryption and decryption roundtrip."""
        secret_symptom = "Patient reports persistent severe heartburn and chest burning after eating spicy foods."
        cipher_text = encrypt_text(secret_symptom)
        self.assertNotEqual(secret_symptom, cipher_text)
        self.assertIsInstance(cipher_text, str)

        decrypted = decrypt_text(cipher_text)
        self.assertEqual(secret_symptom, decrypted)

    def test_02_crypto_json_encryption(self):
        """Test JSON dict encryption and decryption."""
        diet_plan = {
            "foods_to_eat": ["Oatmeal", "Bananas", "Spinach"],
            "foods_to_avoid": ["Spicy chili", "Citrus fruits", "Coffee"],
            "hydration": "2.5 Liters daily"
        }
        cipher = encrypt_json(diet_plan)
        self.assertIsInstance(cipher, str)
        recovered = decrypt_json(cipher)
        self.assertEqual(diet_plan["foods_to_eat"], recovered["foods_to_eat"])
        self.assertEqual(diet_plan["foods_to_avoid"], recovered["foods_to_avoid"])

    def test_03_pii_anonymization(self):
        """Test redaction of sensitive PII (emails, phone numbers)."""
        raw_text = "Contact patient at bharath@example.com or call +1-555-234-5678 regarding chronic fatigue."
        cleaned = anonymize_text(raw_text)
        self.assertNotIn("bharath@example.com", cleaned)
        self.assertNotIn("555-234-5678", cleaned)
        self.assertIn("[REDACTED_EMAIL]", cleaned)
        self.assertIn("[REDACTED_PHONE]", cleaned)

    def test_04_pbkdf2_password_hashing(self):
        """Test salted password hashing and timing-attack resistant verification."""
        password = "SecurePassword123!"
        pwd_hash = hash_password(password)
        self.assertTrue(":" in pwd_hash)
        self.assertTrue(verify_password(pwd_hash, password))
        self.assertFalse(verify_password(pwd_hash, "WrongPassword"))

    def test_05_emergency_red_flag_detection(self):
        """Verify red-flag cardiac and stroke emergencies trigger immediate alerts."""
        cardiac_input = "I am having sudden crushing chest pain and chest tightness radiating to arm."
        alert = detect_emergency_red_flags(cardiac_input)
        self.assertIsNotNone(alert)
        self.assertTrue(alert["is_emergency"])
        self.assertIn("Coronary", alert["condition"])

        stroke_input = "My mother has sudden facial drooping and slurred speech."
        stroke_alert = detect_emergency_red_flags(stroke_input)
        self.assertIsNotNone(stroke_alert)
        self.assertIn("Stroke", stroke_alert["condition"])

    def test_06_gerd_diagnosis_and_diet_protocol(self):
        """Verify GERD symptoms yield accurate diagnosis, gastroenterologist recommendation, diet, and lifestyle."""
        problem = "I have terrible heartburn after dinner, sour taste in mouth, and acid regurgitation when lying down."
        tags = ["Heartburn", "Acid Regurgitation"]
        profile = {"age": "35", "gender": "Male", "severity": 6}

        result = analyze_health_problem(problem, tags, profile)
        primary = result["primary_condition"]

        self.assertIn("Gastroesophageal Reflux", primary["name"])
        self.assertEqual(primary["category"], "Gastroenterology")
        self.assertEqual(primary["specialist"], "Gastroenterologist")
        self.assertGreaterEqual(primary["confidence_score"], 70.0)

        # Verify Diet Protocol
        diet = primary["diet"]
        self.assertIn("foods_to_eat", diet)
        self.assertIn("foods_to_avoid", diet)
        self.assertTrue(any("Oatmeal" in food for food in diet["foods_to_eat"]))
        self.assertTrue(any("Spicy" in food for food in diet["foods_to_avoid"]))

        # Verify Lifestyle Medicine
        lifestyle = primary["lifestyle"]
        self.assertIn("exercise", lifestyle)
        self.assertIn("sleep", lifestyle)
        self.assertTrue("left side" in lifestyle["sleep"].lower())

    def test_07_hypertension_diagnosis(self):
        """Verify cardiovascular hypertension symptom detection."""
        problem = "Persistent headache in back of head, dizziness, and frequent palpitations."
        tags = ["Headache in Back of Head", "Dizziness"]
        profile = {"age": "52", "gender": "Female", "severity": 7, "preexisting": "Hypertension"}

        result = analyze_health_problem(problem, tags, profile)
        primary = result["primary_condition"]
        self.assertIn("Hypertension", primary["name"])
        self.assertEqual(primary["category"], "Cardiovascular")
        self.assertIn("DASH Diet", primary["diet"]["guideline"])

    def test_08_migraine_diagnosis(self):
        """Verify migraine detection with neurological guidance."""
        problem = "Severe throbbing headache on one side of head with sensitivity to light and nausea."
        tags = ["Throbbing Headache", "Sensitivity to Light"]
        profile = {"age": "29", "gender": "Female", "severity": 8}

        result = analyze_health_problem(problem, tags, profile)
        primary = result["primary_condition"]
        self.assertIn("Migraine", primary["name"])
        self.assertEqual(primary["category"], "Neurology")

    def test_09_database_user_and_consultation_lifecycle(self):
        """Test user registration, login, encrypted record saving, reading, and permanent wiping."""
        uname = "testuser_patient_99"
        pwd = "TestSecretPassword#2026"
        name = "Jane Doe"
        profile = {"age": "40", "gender": "Female"}

        success, uid = register_user(uname, pwd, name, profile)
        self.assertTrue(success)

        auth_user = authenticate_user(uname, pwd)
        self.assertIsNotNone(auth_user)
        self.assertEqual(auth_user["full_name"], name)

        # Save consultation
        cid = save_consultation(
            user_id=auth_user["id"],
            symptoms_text="Test symptom report with mild abdominal cramping",
            diagnosis_data={"primary": {"name": "Test Condition", "category": "General"}},
            diet_data={"guideline": "Test Balanced Diet"},
            lifestyle_data={"exercise": "Walking 30 min daily"},
            urgency_level="Routine"
        )
        self.assertGreater(cid, 0)

        # Retrieve and verify decrypted data
        consultations = get_user_consultations(auth_user["id"])
        self.assertGreaterEqual(len(consultations), 1)
        self.assertEqual(consultations[0]["symptoms"], "Test symptom report with mild abdominal cramping")

        # Test Right to be Forgotten (Data Wipe)
        wipe_result = wipe_user_health_data(auth_user["id"])
        self.assertTrue(wipe_result)
        re_auth = authenticate_user(uname, pwd)
        self.assertIsNone(re_auth)

    def test_10_api_routes(self):
        """Test Flask web routes and JSON API responses."""
        # Landing Page
        r1 = self.client.get("/")
        self.assertEqual(r1.status_code, 200)

        # Analyze Page
        r2 = self.client.get("/analyze")
        self.assertEqual(r2.status_code, 200)

        # API Analyze Endpoint
        payload = {
            "problem_description": "Frequent burning urination and urge to urinate",
            "symptom_tags": ["Burning Urination", "Frequent Urination"],
            "severity": 6
        }
        r3 = self.client.post("/api/analyze", json=payload)
        self.assertEqual(r3.status_code, 200)
        data = json.loads(r3.data)
        self.assertIn("primary_condition", data)
        self.assertIn("diet", data["primary_condition"])
        self.assertIn("lifestyle", data["primary_condition"])

    def test_11_pdf_and_dossier_routes(self):
        """Test PDF-ready medical report and comprehensive dossier endpoints."""
        uname = "pdf_test_patient"
        pwd = "SecretPassword!123"
        register_user(uname, pwd, "Alex Patient", {"age": "45", "gender": "Male"})
        user = authenticate_user(uname, pwd)

        cid = save_consultation(
            user_id=user["id"],
            symptoms_text="Severe acid reflux and sour burping",
            diagnosis_data={
                "primary": {
                    "name": "GERD",
                    "category": "Gastroenterology",
                    "specialist": "Gastroenterologist",
                    "confidence_score": 92.0,
                    "explanation": "Acid splashing back into esophagus",
                    "solutions": ["Elevate bed head"]
                },
                "symptoms": ["heartburn"]
            },
            diet_data={"guideline": "Low-acid Mediterranean diet", "foods_to_eat": ["Oats"], "foods_to_avoid": ["Chili"]},
            lifestyle_data={"exercise": "Walking", "sleep": "Left side"},
            urgency_level="Routine"
        )

        with self.client.session_transaction() as sess:
            sess["user_id"] = user["id"]
            sess["username"] = user["username"]
            sess["full_name"] = user["full_name"]
            sess["profile"] = user["profile"]

        # Test individual PDF report view
        r_rec = self.client.get(f"/record/{cid}/print")
        self.assertEqual(r_rec.status_code, 200)
        self.assertIn(b"Clinical Evaluation", r_rec.data)
        self.assertIn(b"Alex Patient", r_rec.data)

        # Test full dossier view
        r_dos = self.client.get("/dossier/print")
        self.assertEqual(r_dos.status_code, 200)
        self.assertIn(b"PATIENT HEALTH DOSSIER", r_dos.data)


if __name__ == "__main__":
    unittest.main()
