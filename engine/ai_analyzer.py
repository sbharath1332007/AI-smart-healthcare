"""
AI Smart Healthcare - Diagnostic & Recommendation Engine
Performs clinical NLP symptom matching, red flag triage, confidence scoring, 
dietary science planning, lifestyle medicine, and optional Gemini LLM enhancement.
"""

import os
import re
import json
from typing import Dict, List, Any, Optional
from .knowledge_base import CONDITIONS_DB, EMERGENCY_RED_FLAGS

try:
    import requests
except ImportError:
    requests = None


def detect_emergency_red_flags(text: str) -> Optional[Dict[str, str]]:
    """Scan patient input for acute life-threatening medical emergencies."""
    normalized_text = text.lower()
    for flag in EMERGENCY_RED_FLAGS:
        for trigger in flag["triggers"]:
            if trigger in normalized_text:
                return {
                    "is_emergency": True,
                    "condition": flag["condition"],
                    "action": flag["action"],
                    "trigger_found": trigger
                }
    return None


def extract_keywords_and_symptoms(text: str, structured_symptoms: List[str]) -> List[str]:
    """Tokenize and extract clinical symptom indicators from free text and inputs."""
    normalized = text.lower()
    symptoms_found = set(s.lower().strip() for s in structured_symptoms if s.strip())

    # Common symptom mapping keywords
    symptom_lexicon = [
        "heartburn", "acid regurgitation", "chest burning", "sour taste in mouth",
        "bloating", "difficulty swallowing", "chronic dry cough", "nausea after meals",
        "burning in upper stomach", "headache in back of head", "dizziness",
        "shortness of breath", "palpitations", "fatigue", "blurred vision",
        "flushing", "nosebleeds", "chest tightness", "pulsing sensation",
        "excessive thirst", "frequent urination", "increased hunger", "unexplained weight loss",
        "chronic fatigue", "blurry vision", "tingling in feet or hands", "slow healing sores",
        "throbbing headache", "one sided head pain", "sensitivity to light", "sensitivity to sound",
        "nausea", "visual aura", "flashing lights", "vomiting", "worse with movement",
        "wheezing", "cough worse at night", "cough with exercise", "rapid breathing",
        "excessive worry", "restlessness", "rapid heartbeat", "muscle tension",
        "trouble sleeping", "insomnia", "difficulty concentrating", "irritability",
        "sweating", "trembling", "nervous stomach", "abdominal cramping", "gas",
        "alternating diarrhea and constipation", "diarrhea after eating", "joint pain",
        "joint stiffness in morning", "cracking in joints", "swelling around joint",
        "persistent productive cough", "yellow mucus", "fever", "sore throat", "runny nose",
        "body aches", "burning sensation when urinating", "frequent urge to urinate",
        "cloudy urine", "pelvic pain", "blood in urine"
    ]

    for item in symptom_lexicon:
        if item in normalized:
            symptoms_found.add(item)
            
    # Single-word helpers
    single_word_matches = {
        "heartburn": "heartburn",
        "cough": "persistent productive cough",
        "fever": "fever",
        "headache": "throbbing headache",
        "bloated": "bloating",
        "bloating": "bloating",
        "thirst": "excessive thirst",
        "thirsty": "excessive thirst",
        "pee": "frequent urination",
        "urination": "frequent urination",
        "wheeze": "wheezing",
        "wheezing": "wheezing",
        "anxious": "excessive worry",
        "anxiety": "excessive worry",
        "cramps": "abdominal cramping",
        "stiffness": "joint stiffness in morning",
        "joint": "joint pain"
    }
    
    for token, mapped_symptom in single_word_matches.items():
        if re.search(rf"\b{token}\b", normalized):
            symptoms_found.add(mapped_symptom)

    return list(symptoms_found)


def analyze_health_problem(
    user_description: str,
    symptom_tags: List[str],
    user_profile: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Main clinical diagnosis, explanation, treatment roadmap, diet & lifestyle generator.
    """
    # 1. Emergency Red-Flag Triage
    full_text = f"{user_description} {' '.join(symptom_tags)}"
    red_flag = detect_emergency_red_flags(full_text)
    
    # 2. Extract Symptoms
    extracted_symptoms = extract_keywords_and_symptoms(user_description, symptom_tags)
    
    # 3. Score matching conditions from Knowledge Base
    scored_conditions = []
    
    for condition in CONDITIONS_DB:
        cond_symptoms = condition["symptoms"]
        matched_points = 0.0
        max_possible_points = sum(cond_symptoms.values())
        matched_items = []
        
        for user_sym in extracted_symptoms:
            for db_sym, weight in cond_symptoms.items():
                if user_sym in db_sym or db_sym in user_sym:
                    matched_points += weight
                    matched_items.append(db_sym)
                    break
        
        # Free-text contextual boost
        norm_desc = user_description.lower()
        if condition["name"].lower() in norm_desc or condition["id"] in norm_desc:
            matched_points += 3.0
            
        for db_sym, weight in cond_symptoms.items():
            if db_sym in norm_desc and db_sym not in matched_items:
                matched_points += weight
                matched_items.append(db_sym)

        # Profile contextual modifiers (e.g. age, severity, preexisting conditions)
        severity = float(user_profile.get("severity", 5))
        if severity >= 7 and condition["urgency"] in ["Urgent", "Emergency"]:
            matched_points *= 1.15
            
        pre_existing = str(user_profile.get("preexisting", "")).lower()
        if "diabetes" in pre_existing and condition["id"] == "type2_diabetes":
            matched_points += 2.0
        if "hypertension" in pre_existing and condition["id"] == "hypertension":
            matched_points += 2.0
        if "asthma" in pre_existing and condition["id"] == "asthma":
            matched_points += 2.0

        if matched_points > 0:
            top_cardinal_weights = sum(sorted(cond_symptoms.values(), reverse=True)[:3])
            confidence = min(96.0, max(45.0, round((matched_points / top_cardinal_weights) * 88.0, 1)))
            scored_conditions.append({
                "condition": condition,
                "score": matched_points,
                "confidence": confidence,
                "matched_symptoms": list(set(matched_items))
            })

    scored_conditions.sort(key=lambda x: x["score"], reverse=True)

    # 4. Fallback if no specific condition matched
    if not scored_conditions:
        primary = {
            "name": "General Symptom Pattern / Unspecified Health Query",
            "category": "General Medicine",
            "urgency": "Routine",
            "specialist": "Primary Care Physician / General Practitioner",
            "explanation": (
                "Based on the provided description, our diagnostic engine detected multiple mild or generalized "
                "symptoms that do not conclusively match a single classic clinical syndrome. These symptoms may "
                "represent acute viral malaise, physical overexertion, dehydration, or early phase immune response."
            ),
            "solutions": [
                "Schedule a routine consultation with a primary care doctor for comprehensive physical exam.",
                "Keep a daily symptom and temperature log.",
                "Ensure restorative sleep (8+ hours) and monitor for any evolving symptoms.",
                "Seek immediate care if symptoms abruptly escalate, or if severe pain develops."
            ],
            "diet": {
                "guideline": "Anti-inflammatory, whole-food restorative nutrition with optimal hydration.",
                "foods_to_eat": ["Steamed vegetables", "Fresh berries", "Bone broths", "Lean protein", "Nuts and seeds"],
                "foods_to_avoid": ["Ultra-processed snacks", "Excess refined sugar", "Alcohol", "High-sodium foods"],
                "meal_timing": "Balanced regular meals every 4-5 hours.",
                "hydration": "2.5 to 3 liters of filtered water daily."
            },
            "lifestyle": {
                "exercise": "Gentle restorative movement such as outdoor walking or light stretching.",
                "sleep": "Aim for 8 to 9 hours of uninterrupted sleep in a dark, quiet room.",
                "stress_management": "Daily 10-minute deep breathing or mindfulness exercises.",
                "habits": "Limit screen time before bed and maintain consistent daily sleep-wake times."
            }
        }
        confidence = 65.0
        secondary_conditions = []
    else:
        top_match = scored_conditions[0]
        primary = top_match["condition"]
        confidence = top_match["confidence"]
        secondary_conditions = [
            {
                "name": sc["condition"]["name"],
                "category": sc["condition"]["category"],
                "confidence": sc["confidence"],
                "specialist": sc["condition"]["specialist"]
            }
            for sc in scored_conditions[1:3]
        ]

    # 5. Optional Gemini LLM Enhancement
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
    ai_enhanced_notes = None
    if gemini_key and requests:
        try:
            ai_enhanced_notes = _call_gemini_api(
                api_key=gemini_key,
                description=user_description,
                primary_name=primary["name"],
                user_profile=user_profile
            )
        except Exception as e:
            ai_enhanced_notes = None

    return {
        "emergency_alert": red_flag,
        "primary_condition": {
            "name": primary["name"],
            "category": primary["category"],
            "urgency": primary["urgency"],
            "specialist": primary["specialist"],
            "confidence_score": confidence,
            "explanation": primary["explanation"],
            "solutions": primary["solutions"],
            "diet": primary["diet"],
            "lifestyle": primary["lifestyle"]
        },
        "secondary_possibilities": secondary_conditions,
        "extracted_symptoms": extracted_symptoms,
        "ai_enhanced_notes": ai_enhanced_notes,
        "disclaimer": (
            "IMPORTANT MEDICAL DISCLAIMER: This AI Smart Healthcare system provides educational information "
            "and health guidance based on clinical knowledge engines. It is NOT a substitute for professional "
            "medical diagnosis, emergency triage, or doctor's prescriptions. Always consult a licensed healthcare "
            "provider for personal medical evaluation."
        )
    }


def _call_gemini_api(api_key: str, description: str, primary_name: str, user_profile: dict) -> Optional[str]:
    """Call Google Gemini API if user configured an API key."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    prompt = (
        f"You are a clinical AI health specialist. A patient reported: '{description}'. "
        f"Patient details: Age {user_profile.get('age', 'N/A')}, Gender {user_profile.get('gender', 'N/A')}, "
        f"Pre-existing: {user_profile.get('preexisting', 'None')}. "
        f"The preliminary diagnostic engine matched: {primary_name}. "
        f"Provide a concise, compassionate 2-paragraph medical explanation and tailored lifestyle advice. "
        f"Include a strong medical safety reminder."
    )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url, json=payload, headers=headers, timeout=8)
    if resp.status_code == 200:
        data = resp.json()
        candidates = data.get("candidates", [])
        if candidates:
            return candidates[0]["content"]["parts"][0]["text"]
    return None
