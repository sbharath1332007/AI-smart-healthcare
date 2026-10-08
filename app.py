"""
AI Smart Healthcare - Core Flask Application
AI-driven medical problem detection, personalized diet & lifestyle prescriptions,
and end-to-end encrypted health data protection.
"""

import os
import json
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from database.db import (
    init_db, register_user, authenticate_user, save_consultation,
    get_user_consultations, wipe_user_health_data, get_recent_security_logs
)
from engine.ai_analyzer import analyze_health_problem
from security.auth import login_required
from security.crypto import anonymize_text

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "smart_healthcare_secure_session_key_98765")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# Ensure DB is initialized
init_db()


@app.context_processor
def inject_user():
    return {
        "current_user": session.get("username"),
        "user_full_name": session.get("full_name")
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze")
def analyze_page():
    return render_template("analyze.html")


@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    data = request.get_json() or {}
    
    problem_text = data.get("problem_description", "").strip()
    symptom_tags = data.get("symptom_tags", [])
    anonymize = data.get("anonymize_mode", False)
    
    if not problem_text and not symptom_tags:
        return jsonify({"error": "Please describe your symptoms or select at least one symptom tag."}), 400

    # Clean / redact PII if user enabled privacy anonymization
    processed_text = anonymize_text(problem_text) if anonymize else problem_text

    user_profile = {
        "age": data.get("age", ""),
        "gender": data.get("gender", ""),
        "height": data.get("height", ""),
        "weight": data.get("weight", ""),
        "severity": data.get("severity", 5),
        "duration": data.get("duration", "Few days"),
        "preexisting": data.get("preexisting", "")
    }

    # Run AI Diagnostic and Care Plan Engine
    analysis_result = analyze_health_problem(
        user_description=processed_text,
        symptom_tags=symptom_tags,
        user_profile=user_profile
    )

    # Save to encrypted vault if logged in and user requested storage
    saved_record_id = None
    save_to_vault = data.get("save_to_vault", True)
    if "user_id" in session and save_to_vault and not anonymize:
        urgency = "Emergency" if analysis_result.get("emergency_alert") else analysis_result["primary_condition"]["urgency"]
        saved_record_id = save_consultation(
            user_id=session["user_id"],
            symptoms_text=processed_text,
            diagnosis_data={
                "primary": analysis_result["primary_condition"],
                "secondary": analysis_result["secondary_possibilities"],
                "symptoms": analysis_result["extracted_symptoms"],
                "ai_notes": analysis_result.get("ai_enhanced_notes")
            },
            diet_data=analysis_result["primary_condition"]["diet"],
            lifestyle_data=analysis_result["primary_condition"]["lifestyle"],
            urgency_level=urgency
        )

    analysis_result["saved_record_id"] = saved_record_id
    analysis_result["is_encrypted_at_rest"] = bool(saved_record_id)
    return jsonify(analysis_result)


@app.route("/dashboard")
@login_required
def dashboard():
    consultations = get_user_consultations(session["user_id"])
    return render_template("dashboard.html", consultations=consultations)


@app.route("/privacy")
def privacy_center():
    user_id = session.get("user_id")
    logs = get_recent_security_logs(user_id) if user_id else []
    return render_template("privacy.html", logs=logs)


@app.route("/auth/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        full_name = request.form.get("full_name", "").strip()
        age = request.form.get("age", "").strip()
        gender = request.form.get("gender", "").strip()
        preexisting = request.form.get("preexisting", "").strip()

        if not username or not password or not full_name:
            flash("All required fields must be completed.", "danger")
            return render_template("register.html")

        profile_data = {
            "age": age,
            "gender": gender,
            "preexisting": preexisting
        }

        success, msg = register_user(username, password, full_name, profile_data)
        if success:
            flash("Registration successful! Your health profile is encrypted with AES-256. Please log in.", "success")
            return redirect(url_for("login"))
        else:
            flash(f"Registration failed: {msg}", "danger")

    return render_template("register.html")


@app.route("/auth/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        user = authenticate_user(username, password)
        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["full_name"] = user["full_name"]
            session["profile"] = user["profile"]
            flash(f"Welcome back, {user['full_name']}! Your encrypted session is active.", "success")
            return redirect(url_for("analyze_page"))
        else:
            flash("Invalid username or password. Please verify credentials.", "danger")

    return render_template("login.html")


@app.route("/auth/logout")
def logout():
    session.clear()
    flash("You have been safely logged out. Encrypted session tokens destroyed.", "info")
    return redirect(url_for("index"))


@app.route("/api/wipe-my-data", methods=["POST"])
@login_required
def wipe_data():
    wipe_user_health_data(session["user_id"])
    session.clear()
    flash("All your medical records, profiles, and encrypted keys have been permanently wiped (Right to be Forgotten).", "warning")
    return redirect(url_for("index"))


@app.route("/api/export-health-data")
@login_required
def export_health_data():
    consultations = get_user_consultations(session["user_id"])
    export_payload = {
        "patient_username": session.get("username"),
        "patient_name": session.get("full_name"),
        "profile": session.get("profile"),
        "export_timestamp": str(os.environ.get("CURRENT_TIME", "2026-10-08")),
        "security": "Exported from AES-256 Decrypted Client Session",
        "total_records": len(consultations),
        "consultations": consultations
    }
    return jsonify(export_payload)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
