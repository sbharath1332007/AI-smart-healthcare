# AI Smart Healthcare

An intelligent, privacy-preserving clinical decision-support and lifestyle medicine platform. Clients describe their symptoms in natural language or structured tags; the AI identifies probable health conditions, delivers an in-depth clinical explanation of what is occurring in the body, charts actionable solutions, and formulates tailored dietary and lifestyle prescriptions—all safeguarded by **AES-256 end-to-end authenticated data encryption**.

---

## Key Pillars

### 1. Clinical Symptom Detection & Triage
- **Natural Language Symptom Processing:** Extracts clinical tokens, duration, severity scale (1–10), and preexisting comorbidities from free-text descriptions.
- **Cardinal Symptom Weighting:** Evaluates presentations against a database of 40+ medical conditions across gastroenterology, cardiology, pulmonology, endocrinology, neurology, rheumatology, and urology.
- **Emergency Red-Flag Screening:** Instantly intercepts life-threatening emergencies (acute coronary syndrome, stroke FAST symptoms, anaphylaxis, severe respiratory failure) with urgent dispatch protocols.
- **Optional Gemini LLM Augmentation:** Can augment responses using Google Gemini API (`GEMINI_API_KEY`) while gracefully running fully offline with the built-in evidence-based clinical engine.

### 2. In-Depth Explanation & Actionable Solutions
- **Pathophysiology Demystified:** Explains root biological mechanisms and why specific symptoms manifest.
- **Clinical Solutions & Roadmap:** Step-by-step guidance, including recommended medical specialist referrals (e.g., Gastroenterologist, Pulmonologist, Neurologist), OTC recommendations, home supportive care, and danger signs requiring emergency care.

### 3. Personalized Diet & Lifestyle Medicine
- **Tailored Dietary Protocols:** Specific therapeutic diets (e.g., Low-Acid Mediterranean, DASH Diet, Low-GI Diabetic, Low-FODMAP).
- **Foods to Eat & Strictly Avoid:** Evidence-based lists of healing superfoods and symptomatic trigger foods.
- **Meal Schedule & Hydration Targets:** Practical timing recommendations and daily fluid intake guidelines.
- **Personalized Lifestyle Routines:** Targeted exercise regimens, posture and sleep hygiene (e.g., left-lateral sleep for GERD), vagal stress-reduction exercises, and environmental adjustments.

### 4. Zero-Trust Patient Data Protection
- **AES-256 Fernet Encryption:** All Protected Health Information (PHI)—including patient names, ages, symptom histories, diagnoses, diet plans, and lifestyle records—is encrypted at rest before hitting disk.
- **PBKDF2 Password Salting:** Passwords hashed with 100,000 iterations of PBKDF2-HMAC-SHA256 and unique 16-byte random salts.
- **Patient Anonymization Mode:** One-click toggle to redact personal identifiers (emails, phone numbers, IDs) during intake.
- **Right to Be Forgotten (GDPR Art. 17):** Permanent one-click cryptographic data purge to permanently delete health records and account history.
- **Security Audit Trail:** Immutable event logs tracking encrypted writes and reads.

---

## Project Structure

```
AI-smart-healthcare/
├── app.py                     # Main Flask web application and API endpoints
├── test_suite.py              # Automated test suite (crypto, auth, clinical engine, API)
├── requirements.txt           # Python dependencies (Flask, Cryptography, Requests, Werkzeug)
├── .gitignore                 # Excludes local databases, encryption keys, and environment files
├── security/
│   ├── crypto.py              # AES-256 Fernet encryption, decryption, and PII anonymization
│   └── auth.py                # PBKDF2 password hashing, verification, and session control
├── engine/
│   ├── knowledge_base.py      # Clinical condition database, symptom weights, diet & lifestyle
│   └── ai_analyzer.py         # Diagnostic NLP engine, red-flag triage, and Gemini integration
├── database/
│   └── db.py                  # SQLite encrypted schema, consultation storage, and audit logs
├── templates/
│   ├── base.html              # Responsive layout with Tailwind CSS & Lucide icons
│   ├── index.html             # Landing page with interactive feature showcase
│   ├── analyze.html           # Clinical symptom intake wizard & care plan viewer
│   ├── dashboard.html         # Decrypted personal health vault and consultation history
│   ├── privacy.html           # Cryptography specifications, audit logs, and data wipe
│   ├── login.html             # Patient authentication portal
│   └── register.html          # New patient onboarding with encrypted profile
└── instance/                  # Local encrypted database and key storage (gitignored)
```

---

## Quickstart Guide

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.12)
- Git

### 2. Installation
```powershell
# Clone the repository
git clone https://github.com/sbharath1332007/AI-smart-healthcare.git
cd AI-smart-healthcare

# Install dependencies
pip install -r requirements.txt
```

### 3. Running the Application
```powershell
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

### 4. Running the Test Suite
```powershell
python test_suite.py
```

### 5. Optional Gemini AI Enhancement
To enable advanced generative clinical reasoning, set your Gemini API key:
```powershell
$env:GEMINI_API_KEY="your_api_key_here"
python app.py
```
*(The system works completely out of the box even without an API key using the built-in clinical engine.)*

---

## Security & Compliance Specifications

| Security Layer | Implementation |
|---|---|
| **Data Encryption at Rest** | AES-128-CBC with PKCS7 padding & HMAC-SHA256 (Fernet / AES-256) |
| **Password Storage** | PBKDF2-HMAC-SHA256 (100,000 iterations + 16-byte random salt) |
| **Session Security** | HTTP-Only, SameSite=Lax session cookies |
| **PII Redaction** | Automated regex sanitization for emails, phone numbers, and IDs |
| **Data Sovereignty** | Exportable JSON health records and permanent "Right to be Forgotten" wipe |

---

## Medical Disclaimer

> **IMPORTANT:** AI Smart Healthcare provides educational guidance and clinical decision-support only. It is **not** a replacement for professional clinical diagnosis, physical examination, emergency triage, or doctor's prescription. If experiencing symptoms indicative of a medical emergency (such as crushing chest pain, sudden paralysis, or severe respiratory distress), immediately contact emergency dispatch (911 / 112 / 999).
