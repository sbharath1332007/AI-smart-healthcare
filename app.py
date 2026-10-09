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
from engine.report_analyzer import analyze_uploaded_medical_report
from security.auth import login_required
from security.crypto import anonymize_text
from werkzeug.utils import secure_filename

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


@app.route("/api/analyze-report", methods=["POST"])
def api_analyze_report():
    if "report_file" not in request.files:
        return jsonify({"error": "No report file was provided. Please upload a PDF or photo of your medical report."}), 400
    
    file = request.files["report_file"]
    if not file or file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    filename = secure_filename(file.filename) or "medical_report.pdf"
    file_bytes = file.read()

    if len(file_bytes) == 0:
        return jsonify({"error": "Uploaded file is empty."}), 400

    if len(file_bytes) > 16 * 1024 * 1024:
        return jsonify({"error": "File size exceeds 16MB limit."}), 400

    # User profile and notes
    user_profile = {
        "age": request.form.get("age", ""),
        "gender": request.form.get("gender", ""),
        "preexisting": request.form.get("preexisting", "")
    }
    patient_notes = request.form.get("patient_notes", "").strip()
    gemini_key = request.form.get("api_key", "").strip()
    save_to_vault = request.form.get("save_to_vault", "true").lower() == "true"

    analysis_result = analyze_uploaded_medical_report(
        file_bytes=file_bytes,
        filename=filename,
        mime_type=file.mimetype or "application/octet-stream",
        user_profile=user_profile,
        patient_notes=patient_notes,
        gemini_api_key=gemini_key
    )

    # Save to encrypted vault if authenticated
    saved_record_id = None
    if "user_id" in session and save_to_vault:
        urgency = "Emergency" if analysis_result.get("emergency_alert") else analysis_result["primary_condition"]["urgency"]
        narrative = f"[Medical Report: {filename}] " + (patient_notes if patient_notes else analysis_result["primary_condition"]["name"])
        saved_record_id = save_consultation(
            user_id=session["user_id"],
            symptoms_text=narrative,
            diagnosis_data={
                "primary": analysis_result["primary_condition"],
                "secondary": analysis_result.get("secondary_possibilities", []),
                "lab_findings": analysis_result.get("lab_findings", []),
                "report_filename": filename,
                "report_type": analysis_result.get("report_type"),
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
    return render_template(
        "dashboard.html",
        consultations=consultations,
        patient_name=session.get("full_name"),
        username=session.get("username"),
        profile=session.get("profile", {})
    )


@app.route("/record/<int:record_id>/print")
@login_required
def print_medical_record(record_id):
    consultations = get_user_consultations(session["user_id"])
    target = None
    for c in consultations:
        if c["id"] == record_id:
            target = c
            break
    if not target:
        flash("Medical record not found.", "danger")
        return redirect(url_for("dashboard"))
    
    return render_template(
        "medical_report.html",
        record=target,
        patient_name=session.get("full_name"),
        username=session.get("username"),
        profile=session.get("profile", {})
    )


@app.route("/dossier/print")
@login_required
def print_complete_dossier():
    consultations = get_user_consultations(session["user_id"])
    return render_template(
        "medical_dossier.html",
        consultations=consultations,
        patient_name=session.get("full_name"),
        username=session.get("username"),
        profile=session.get("profile", {})
    )


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
            user = authenticate_user(username, password)
            if user:
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                session["full_name"] = user["full_name"]
                session["profile"] = user["profile"]
            flash(f"Welcome, {full_name}! Your encrypted health account has been created.", "success")
            return redirect(url_for("analyze_page"))
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


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
