"""
AI Smart Healthcare - Voice Assistant Engine
Handles speech script synthesis, audio transcription & multimodal voice analysis,
and conversational clinical voice responses.
"""

import os
import json
import base64
import re
from typing import Dict, Any, Optional

try:
    import requests
except ImportError:
    requests = None

from engine.ai_analyzer import analyze_health_problem, detect_emergency_red_flags


def generate_spoken_voice_script(analysis_result: Dict[str, Any]) -> str:
    """
    Synthesizes a fluent, empathetic, and clear spoken-voice script
    intended for Text-To-Speech (TTS) readout to the patient.
    """
    if not analysis_result:
        return "No analysis data is available to read."

    # Emergency check first
    emergency_alert = analysis_result.get("emergency_alert")
    if emergency_alert:
        return (
            f"Urgent clinical alert. Your reported symptoms indicate potential emergency red flags: "
            f"{emergency_alert.get('message', 'Immediate medical attention is recommended')}. "
            f"Recommended immediate action: {emergency_alert.get('action', 'Call 911 or visit the nearest emergency room immediately')}. "
            f"Please do not wait."
        )

    primary = analysis_result.get("primary_condition", {})
    name = primary.get("name", "Health Condition")
    confidence = primary.get("confidence_score", 85)
    urgency = primary.get("urgency", "Routine")
    specialist = primary.get("specialist", "General Physician")
    explanation = primary.get("explanation", "")
    solutions = primary.get("solutions", [])
    diet = primary.get("diet", {})
    lifestyle = primary.get("lifestyle", {})

    # Build conversational sentences
    parts = []
    parts.append(f"Hello. Based on your symptoms and clinical evaluation, our AI analysis identified a primary possibility of {name}, with an estimated confidence of {confidence:.1f} percent.")
    parts.append(f"This condition is categorized as {urgency} priority. We recommend consulting a {specialist} for formal evaluation.")

    if explanation:
        # Take first 1-2 sentences of explanation
        explanation_sentences = re.split(r'(?<=[.!?])\s+', explanation)
        brief_explanation = " ".join(explanation_sentences[:2])
        parts.append(f"Regarding what is happening: {brief_explanation}")

    if solutions and len(solutions) > 0:
        clean_sol1 = re.sub(r'^[0-9\.\-\*\s]+', '', solutions[0]).strip()
        parts.append(f"Immediate medical step: {clean_sol1}.")

    guideline = diet.get("guideline", "")
    foods_to_eat = diet.get("foods_to_eat", [])
    foods_to_avoid = diet.get("foods_to_avoid", [])
    if guideline:
        eat_str = ", ".join(foods_to_eat[:3]) if foods_to_eat else ""
        avoid_str = ", ".join(foods_to_avoid[:3]) if foods_to_avoid else ""
        diet_sentence = f"For dietary care: {guideline}."
        if eat_str:
            diet_sentence += f" Prioritize foods like {eat_str}."
        if avoid_str:
            diet_sentence += f" Avoid {avoid_str}."
        parts.append(diet_sentence)

    habits = lifestyle.get("habits", "")
    if habits:
        parts.append(f"Recommended lifestyle habit: {habits}.")

    parts.append("You can review your detailed care plan, download the complete PDF report, or revisit this consultation anytime in your health records vault.")

    return " ".join(parts)


def transcribe_and_analyze_audio_gemini(
    audio_bytes: bytes,
    mime_type: str,
    user_profile: Optional[Dict[str, Any]] = None,
    gemini_api_key: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Submits recorded user audio directly to Google Gemini Flash
    for multimodal speech transcription, clinical symptom extraction,
    and structured diagnosis.
    """
    if not requests or not audio_bytes:
        return None

    api_key = gemini_api_key or os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        return None

    user_profile = user_profile or {}

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        base64_audio = base64.b64encode(audio_bytes).decode("utf-8")

        prompt = (
            f"You are an empathetic, clinical Voice Assistant AI. Listen to the user's spoken voice recording describing their health problem. "
            f"Patient Context: Age: {user_profile.get('age', 'N/A')}, Gender: {user_profile.get('gender', 'N/A')}, "
            f"Pre-existing: {user_profile.get('preexisting', 'None')}.\n\n"
            f"Tasks:\n"
            f"1. Accurately transcribe what the patient said into 'transcribed_text'.\n"
            f"2. Extract primary symptoms.\n"
            f"3. Diagnose the probable medical condition with specialist referral, medical solutions, tailored diet, and lifestyle.\n\n"
            f"Return strictly as a JSON object with this exact structure:\n"
            f"{{\n"
            f'  "transcribed_text": "string of verbatim transcribed speech",\n'
            f'  "extracted_symptoms": ["symptom1", "symptom2"],\n'
            f'  "primary_condition": {{\n'
            f'     "name": "string condition name",\n'
            f'     "category": "string category",\n'
            f'     "urgency": "Routine|Urgent|Emergency",\n'
            f'     "specialist": "string specialist",\n'
            f'     "confidence_score": 92.0,\n'
            f'     "explanation": "string explanation",\n'
            f'     "solutions": ["step 1", "step 2", "step 3"],\n'
            f'     "diet": {{\n'
            f'        "guideline": "string",\n'
            f'        "foods_to_eat": ["food 1", "food 2"],\n'
            f'        "foods_to_avoid": ["food 1", "food 2"],\n'
            f'        "meal_timing": "string",\n'
            f'        "hydration": "string"\n'
            f"     }},\n"
            f'     "lifestyle": {{\n'
            f'        "exercise": "string",\n'
            f'        "sleep": "string",\n'
            f'        "stress_management": "string",\n'
            f'        "habits": "string"\n'
            f"     }}\n"
            f"  }},\n"
            f'  "emergency_alert": null,\n'
            f'  "secondary_possibilities": []\n'
            f"}}\n"
            f"Do not include any markdown fences or preamble outside the valid JSON."
        )

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": mime_type,
                                "data": base64_audio
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "response_mime_type": "application/json",
                "temperature": 0.2
            }
        }

        resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=25)
        if resp.status_code == 200:
            result_json = resp.json()
            candidates = result_json.get("candidates", [])
            if candidates:
                raw_text = candidates[0]["content"]["parts"][0]["text"].strip()
                if raw_text.startswith("```json"):
                    raw_text = raw_text[7:]
                if raw_text.startswith("```"):
                    raw_text = raw_text[3:]
                if raw_text.endswith("```"):
                    raw_text = raw_text[:-3]
                parsed = json.loads(raw_text.strip())
                # Generate spoken script
                parsed["voice_summary_spoken"] = generate_spoken_voice_script(parsed)
                parsed["is_voice_consultation"] = True
                return parsed
    except Exception as e:
        print(f"Gemini audio processing exception: {e}")

    return None


def process_voice_consultation(
    spoken_text: str,
    audio_bytes: Optional[bytes] = None,
    mime_type: Optional[str] = None,
    user_profile: Optional[Dict[str, Any]] = None,
    gemini_api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Main orchestrator for Voice Consultation:
    1. If raw audio was provided with an API key, attempts Gemini audio transcription & analysis.
    2. Otherwise, processes the spoken_text with the full clinical intelligence engine.
    3. Adds conversational spoken voice script for TTS read-aloud.
    """
    user_profile = user_profile or {}

    # Try multimodal audio if bytes provided
    if audio_bytes and len(audio_bytes) > 0 and mime_type:
        gemini_result = transcribe_and_analyze_audio_gemini(
            audio_bytes=audio_bytes,
            mime_type=mime_type,
            user_profile=user_profile,
            gemini_api_key=gemini_api_key
        )
        if gemini_result:
            return gemini_result

    # Standard clinical analysis on spoken text
    text_to_analyze = spoken_text.strip() if spoken_text else ""
    if not text_to_analyze:
        text_to_analyze = "General physical consultation"

    result = analyze_health_problem(
        user_description=text_to_analyze,
        symptom_tags=[],
        user_profile=user_profile
    )

    result["transcribed_text"] = spoken_text.strip()
    result["is_voice_consultation"] = True
    result["voice_summary_spoken"] = generate_spoken_voice_script(result)

    return result
