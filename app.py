import os
import re
from flask import Flask, render_template, request, jsonify, session
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "brandguard_secure_fallback_key")

# MongoDB Atlas URI configuration
MONGO_URI = os.getenv("MONGO_URI")
db = None
mongo_client = None

try:
    if MONGO_URI:
        mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        mongo_client.admin.command('ping')
        db = mongo_client["brandguard_db"]
        print("Connected to MongoDB Atlas successfully!")
    else:
        print("Warning: MONGO_URI not found in environment. Running with in-memory fallback.")
except Exception as e:
    print(f"MongoDB connection failed: {e}. Running with in-memory fallback.")

# In-memory fallback audit logs if DB is unavailable
in_memory_logs = []

# Banned absolute claims and trigger words (Layer 1: Deterministic Regex)
BANNED_REGEX_TERMS = [
    r"\b100%\b",
    r"\bguaranteed\b",
    r"\bbest\b",
    r"\brisk-free\b",
    r"\bcheapest\b",
    r"\bcure\b",
    r"\bmiracle\b"
]

# High-risk manipulative/sarcastic triggers (Layer 2: Semantic Fallback)
SEMANTIC_TRIGGER_WORDS = [
    "trust me",
    "definitely not a scam",
    "wink wink",
    "no questions asked",
    "foolproof"
]

@app.route("/")
def index():
    if "role" not in session:
        session["role"] = "MARKETER"
    return render_template("index.html", current_role=session.get("role"))

@app.route("/set-role", methods=["POST"])
def set_role():
    data = request.get_json() or {}
    role = data.get("role", "MARKETER")
    if role in ["MARKETER", "LEGAL_REVIEWER", "ADMIN"]:
        session["role"] = role
        return jsonify({"status": "success", "role": role})
    return jsonify({"status": "error", "message": "Invalid role"}), 400

@app.route("/api/audit", methods=["POST"])
def audit_content():
    data = request.get_json() or {}
    text = data.get("text", "").strip()

    # Graceful Empty State Validation
    if not text:
        return jsonify({
            "error": "Please enter marketing copy or ad text to run the compliance audit."
        }), 400
    
    # Robust Smart Validation: Extract actual valid words (at least 2 letters each, min 2 words)
    valid_words = re.findall(r'[a-zA-Z]{2,}', text)
    if len(valid_words) < 2:
        return jsonify({
            "error": "Invalid or insufficient marketing copy. Please enter a meaningful sentence with actual words."
        }), 400

    violations = []
    score = 100
    rewritten_text = text

    # Layer 1: Deterministic Regex Rule Engine
    for pattern in BANNED_REGEX_TERMS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            for m in set(matches):
                violations.append(f"Prohibited absolute claim detected: '{m}'")
                score -= 20
                rewritten_text = re.sub(re.escape(m), "[verified]", rewritten_text, flags=re.IGNORECASE)

    # Layer 2: Semantic Tone & Manipulative Fallback Layer
    text_lower = text.lower()
    for trigger in SEMANTIC_TRIGGER_WORDS:
        if trigger in text_lower:
            violations.append(f"High-risk deceptive framing detected: '{trigger}'")
            score -= 15
            rewritten_text = rewritten_text.replace(trigger, "[reviewed phrasing]")

    score = max(0, score)

    audit_record = {
        "text": text,
        "score": score,
        "violations": violations,
        "rewritten_text": rewritten_text,
        "role": session.get("role", "MARKETER")
    }

    # Persistent Cloud Integration with Graceful In-Memory Redundancy
    try:
        if db is not None:
            db.audits.insert_one(audit_record)
        else:
            in_memory_logs.append(audit_record)
    except Exception as e:
        print(f"Database write error, falling back to memory: {e}")
        in_memory_logs.append(audit_record)

    return jsonify({
        "status": "success",
        "score": score,
        "violations": violations,
        "rewritten_text": rewritten_text,
        "active_role": session.get("role", "MARKETER")
    })

@app.route("/api/export-audit", methods=["GET"])
def export_audit():
    try:
        if db is not None:
            records = list(db.audits.find({}, {"_id": 0}))
        else:
            records = in_memory_logs
    except Exception:
        records = in_memory_logs

    return jsonify({
        "project": "BrandGuard-AI",
        "team": "SOLOSYNTAX",
        "total_audits": len(records),
        "audit_logs": records
    })

@app.route("/api/clear-audits", methods=["POST"])
def clear_audits():
    global in_memory_logs
    in_memory_logs = []
    try:
        if db is not None:
            db.audits.delete_many({})
    except Exception as e:
        print(f"Error clearing DB: {e}")
    return jsonify({"status": "success", "message": "All audit logs cleared successfully!"})

@app.route("/api/v1/webhook-audit", methods=["POST"])
def webhook_audit():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Unauthorized: Missing or invalid Bearer token"}), 401

    data = request.get_json() or {}
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "Text payload is required"}), 400

    score = 100
    if "guaranteed" in text.lower() or "100%" in text:
        score = 40

    return jsonify({
        "webhook_status": "audited",
        "score": score,
        "message": "Content scanned successfully via CMS webhook gateway."
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)