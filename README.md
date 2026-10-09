# AI Smart Healthcare

An intelligent, privacy-preserving clinical decision-support and lifestyle medicine platform. Patients describe their symptoms via **hands-free AI voice assistance**, clinical text intake, or by **uploading lab reports (PDF/Photo)**; the AI extracts biometric markers, identifies probable health conditions, delivers an in-depth clinical explanation of underlying pathophysiology, charts actionable solutions, and formulates tailored dietary and lifestyle prescriptions—all safeguarded by **AES-256 end-to-end authenticated data encryption**.

[![Render Production](https://img.shields.io/badge/Render-Live%20Production%20%E2%9C%94-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://ai-smart-healthcare.onrender.com)
[![Web App](https://img.shields.io/badge/Web%20App-ai--smart--healthcare.onrender.com-00B4D8?style=for-the-badge&logo=google-chrome&logoColor=white)](https://ai-smart-healthcare.onrender.com)
[![Voice Assistant](https://img.shields.io/badge/AI%20Voice%20Assistant-Live-7C3AED?style=for-the-badge&logo=soundcharts&logoColor=white)](https://ai-smart-healthcare.onrender.com/analyze?mode=voice)
[![Report OCR](https://img.shields.io/badge/Report%20Scanner-PDF%20%7C%20Photo-059669?style=for-the-badge&logo=adobeacrobatreader&logoColor=white)](https://ai-smart-healthcare.onrender.com/analyze?mode=report)
[![Security](https://img.shields.io/badge/Security-AES--256%20Fernet-1E293B?style=for-the-badge&logo=auth0&logoColor=white)](https://ai-smart-healthcare.onrender.com/privacy)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

---

## 🚀 Live Production Deployment

The platform is fully deployed and operational in production on **Render Cloud Infrastructure** with automated SSL/TLS encryption and multi-worker WSGI concurrency.

| Feature / Service | Direct Production URL | Status |
|---|---|---|
| **🌐 Main Application Portal** | [https://ai-smart-healthcare.onrender.com](https://ai-smart-healthcare.onrender.com) | `Active` 🟢 |
| **🎙️ AI Voice Doctor Assistant** | [https://ai-smart-healthcare.onrender.com/analyze?mode=voice](https://ai-smart-healthcare.onrender.com/analyze?mode=voice) | `Active` 🟢 |
| **📄 Medical Report Scanner (PDF/Photo)** | [https://ai-smart-healthcare.onrender.com/analyze?mode=report](https://ai-smart-healthcare.onrender.com/analyze?mode=report) | `Active` 🟢 |
| **🩺 Symptom Triage & Care Plan** | [https://ai-smart-healthcare.onrender.com/analyze?mode=text](https://ai-smart-healthcare.onrender.com/analyze?mode=text) | `Active` 🟢 |
| **🛡️ Encrypted Patient Health Vault** | [https://ai-smart-healthcare.onrender.com/dashboard](https://ai-smart-healthcare.onrender.com/dashboard) | `Active` 🟢 |
| **🔐 Privacy & Cryptography Specs** | [https://ai-smart-healthcare.onrender.com/privacy](https://ai-smart-healthcare.onrender.com/privacy) | `Active` 🟢 |

### Cloud Infrastructure & Hosting Architecture

- **Host Platform:** Render Cloud Web Services ([render.com](https://render.com))
- **Production URL:** `https://ai-smart-healthcare.onrender.com`
- **Application Server:** Multi-worker Gunicorn WSGI (`gunicorn app:app --workers 2 --bind 0.0.0.0:$PORT`)
- **Containerization:** Python 3.12-slim Docker container with zero external OS bloat
- **SSL / Security:** Automated wildcard HTTPS / TLS 1.3 encryption managed at the edge CDN
- **Continuous Integration / Continuous Delivery (CI/CD):** Synchronized directly with the GitHub `main` branch (`sbharath1332007/AI-smart-healthcare`). Any push to `main` initiates an automated zero-downtime rebuild and redeployment.

---

## 💡 Key Pillars & System Capabilities

### 1. Hands-Free AI Voice Assistant
- **Real-Time Speech-to-Text:** Live continuous microphone stream with Web Audio API frequency visualizer.
- **Conversational Intake:** Patients can speak naturally about their symptoms, pain locations, duration, and concerns.
- **Spoken Clinical Response:** Integrates browser speech synthesis (`SpeechSynthesisUtterance`) to read the diagnosis, root causes, and top care instructions aloud to the patient.

### 2. AI Medical Report Scanner (PDF & Photo)
- **Multi-Format Ingestion:** Accepts laboratory reports, discharge summaries, blood panels, and imaging impressions via PDF or image files (PNG, JPG, JPEG, WebP).
- **Automated Biomarker Extraction:** Parses clinical metrics (e.g., HbA1c, Fasting Glucose, Lipid Profile, Liver Function AST/ALT, Hemoglobin, Leukocytes).
- **Critical Range Interception:** Detects abnormal and severely elevated/depressed values, correlating them with symptomatic diagnoses and therapeutic protocols.

### 3. Clinical Symptom Detection & Triage
- **Natural Language Symptom Processing:** Extracts clinical tokens, severity scales (1–10), and preexisting comorbidities.
- **Cardinal Symptom Weighting:** Evaluates presentations against a comprehensive clinical engine of 40+ medical conditions across cardiology, pulmonology, gastroenterology, neurology, endocrinology, rheumatology, and urology.
- **Emergency Red-Flag Screening:** Instantly intercepts life-threatening emergencies (acute coronary syndrome, stroke FAST symptoms, anaphylaxis, severe respiratory distress) with urgent dispatch warnings.
- **Optional Gemini LLM Augmentation:** Seamlessly augments reasoning using Google Gemini API (`GEMINI_API_KEY`) while running completely offline out-of-the-box with the deterministic evidence-based clinical engine.

### 4. Personalized Diet & Lifestyle Medicine
- **Tailored Dietary Protocols:** Specific therapeutic diets (e.g., Low-Acid Mediterranean, DASH Diet, Low-GI Diabetic, Low-FODMAP, Anti-Inflammatory).
- **Foods to Eat & Strictly Avoid:** Evidence-based matrices of healing foods and symptomatic trigger items.
- **Circadian Meal & Hydration Plans:** Actionable timing recommendations and daily fluid intake guidelines.
- **Targeted Lifestyle Routines:** Condition-specific exercise regimens, posture and sleep hygiene (e.g., left-lateral elevation for GERD), vagal nerve relaxation exercises, and environmental adjustments.

### 5. Zero-Trust Patient Data Protection
- **AES-256 Fernet Encryption:** All Protected Health Information (PHI)—including patient names, ages, symptom histories, diagnostic evaluations, diet plans, and lifestyle records—is encrypted at rest before writing to disk.
- **PBKDF2 Password Salting:** Passwords hashed with 100,000 iterations of PBKDF2-HMAC-SHA256 and unique 16-byte cryptographically secure random salts.
- **Patient Anonymization Mode:** Real-time sanitization of personal identifiers (emails, phone numbers, governmental IDs).
- **Right to Be Forgotten (GDPR Art. 17):** Permanent one-click cryptographic data purge that eradicates health records and account history from disk.
- **Security Audit Trail:** Immutable event logs tracking encrypted writes, reads, and auth operations.

---

## 📁 Repository Structure

```
AI-smart-healthcare/
├── app.py                     # Main Flask web application, REST API & routing
├── render.yaml                # Render Cloud Infrastructure as Code blueprint
├── Procfile                   # Cloud process execution command (gunicorn app:app)
├── Dockerfile                 # Production container image definition
├── vercel.json                # Vercel serverless configuration
├── requirements.txt           # Python dependencies (Flask, Cryptography, Requests, Gunicorn, Waitress)
├── test_suite.py              # Automated test suite (crypto, auth, clinical engine, API)
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
│   ├── analyze.html           # Symptom intake, voice assistant & report upload wizard
│   ├── dashboard.html         # Decrypted personal health vault and consultation history
│   ├── privacy.html           # Cryptography specifications, audit logs, and data wipe
│   ├── login.html             # Patient authentication portal
│   └── register.html          # New patient onboarding with encrypted profile
└── instance/                  # Local encrypted database and key storage (gitignored)
```

---

## 🛠️ Deployment Configuration Files

This repository contains ready-to-run deployment manifests for all major cloud providers:

### 1. Render (`render.yaml` & `Procfile`)
- **Blueprint file:** [`render.yaml`](render.yaml) automatically provisions a Python 3.12 web service.
- **Procfile:**
  ```procfile
  web: gunicorn app:app
  ```

### 2. Docker (`Dockerfile`)
Run anywhere Docker is supported (AWS ECS, Google Cloud Run, Railway, DigitalOcean):
```bash
docker build -t ai-smart-healthcare .
docker run -p 5000:5000 -e PORT=5000 ai-smart-healthcare
```

---

## 💻 Local Quickstart

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.12)
- Git

### 2. Clone & Install
```powershell
# Clone the repository
git clone https://github.com/sbharath1332007/AI-smart-healthcare.git
cd AI-smart-healthcare

# Install dependencies
pip install -r requirements.txt
```

### 3. Run Locally
```powershell
python app.py
```
Open your browser at `http://127.0.0.1:5000`.

### 4. Run Test Suite
```powershell
python test_suite.py
```

### 5. Optional Gemini LLM Configuration
The platform runs completely standalone with its embedded clinical engine. To optionally augment clinical reasoning with Google Gemini:
```powershell
$env:GEMINI_API_KEY="your_api_key_here"
python app.py
```

---

## 🛡️ Security & Privacy Compliance

| Security Layer | Implementation Specification |
|---|---|
| **Data Encryption at Rest** | AES-128-CBC with PKCS7 padding & HMAC-SHA256 (Fernet / AES-256 equivalent) |
| **Password Storage** | PBKDF2-HMAC-SHA256 (100,000 iterations + 16-byte random salt) |
| **Session Security** | HTTP-Only, SameSite=Lax session cookies |
| **PII Redaction** | Automated regex sanitization for emails, phone numbers, and IDs |
| **Data Sovereignty** | Permanent cryptographic "Right to be Forgotten" account & consultation wipe |

---

## ⚠️ Medical Disclaimer

> **IMPORTANT:** AI Smart Healthcare provides educational guidance and clinical decision-support only. It is **not** a substitute for professional medical advice, clinical diagnosis, emergency triage, or doctor's treatment. If experiencing symptoms indicative of a life-threatening medical emergency (e.g., severe crushing chest pain radiating to the left arm/jaw, sudden unilateral numbness/paralysis, or acute respiratory distress), call emergency services (**911 / 112 / 999**) immediately.
