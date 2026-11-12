from datetime import datetime
import os
import re
from flask import Flask, jsonify, render_template, request, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "brandguard_secret_key_solosyntax_2026"

# In-memory storage fallback for audit logs when DB is in fallback mode
fallback_audit_logs = []

# MongoDB Atlas Connection Setup with Fallback Mode
MONGO_URI = os.environ.get(
    "MONGO_URI", "mongodb+srv://cluster.mongodb.net/brandguard"
)
db_connected = False
try:
  client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
  client.admin.command("ping")
  db = client["brandguard_db"]
  audit_collection = db["audit_logs"]
  db_connected = True
  print("Connected to MongoDB Atlas successfully!")
except Exception as e:
  print(f"Warning: MongoDB connection failed ({e}). Running in fallback mode.")
  db_connected = False

# Default Banned Words & Absolute Rules
BANNED_WORDS = [
    "100%",
    "guaranteed",
    "best",
    "risk-free",
    "cheapest",
    "cure",
    "miracle",
    "instant",
]


def clean_and_rewrite(text, banned_words):
  """Replaces prohibited terms using strict word boundaries to prevent

  substring bugs (e.g., preventing 'secure' from matching 'sec').
  """
  for word in banned_words:
    # \b ensures exact whole-word matching
    pattern = r"\b" + re.escape(word) + r"\b"
    text = re.sub(pattern, "[verified]", text, flags=re.IGNORECASE)
  return text


def semantic_llm_fallback_scan(text):
  """Simulates a multi-model LLM compliance layer for sarcasm,

  manipulative tone, and high-risk persuasive framing.
  """
  violations = []
  lower_text = text.lower()
  sarcasm_triggers = ["trust me", "definitely not a scam", "wink wink"]
  for trigger in sarcasm_triggers:
    if trigger in lower_text:
      violations.append(
          f'"{trigger}": Potential sarcastic or high-risk persuasive framing'
          " detected by LLM Semantic Layer."
      )
  return violations


@app.route("/")
def index():
  role = session.get("role", "MARKETER")
  return render_template("index.html", role=role, db_status=db_connected)


@app.route("/set-role", methods=["POST"])
def set_role():
  data = request.get_json() or {}
  new_role = data.get("role", "MARKETER")
  if new_role in ["MARKETER", "LEGAL_REVIEWER", "ADMIN"]:
    session["role"] = new_role
    return jsonify({"success": True, "role": new_role})
  return jsonify({"success": False, "error": "Invalid role"}), 400


@app.route("/api/audit", methods=["POST"])
def audit_text():
  data = request.get_json() or {}
  text = data.get("text", "")
  role = session.get("role", "MARKETER")

  if not text:
    return jsonify({"error": "No text provided"}), 400

  violations = []

  # Check regex rule violations with strict word boundaries
  for word in BANNED_WORDS:
    pattern = r"\b" + re.escape(word) + r"\b"
    if re.search(pattern, text, re.IGNORECASE):
      violations.append(
          f'"{word}": Absolute or prohibited marketing claim detected (Regex'
          " Rule)."
      )

  # Check semantic LLM fallback violations
  semantic_violations = semantic_llm_fallback_scan(text)
  violations.extend(semantic_violations)

  # Calculate score (100 base, minus 15 per violation, min 20)
  score = max(20, 100 - (len(violations) * 15))
  if len(violations) == 0:
    score = 100

  # Generate suggested rewrite using safe whole-word boundary substitution
  suggested_rewrite = clean_and_rewrite(text, BANNED_WORDS)

  audit_entry = {
      "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
      "role": role,
      "original_text": text,
      "score": score,
      "violations_count": len(violations),
      "violations": violations,
      "suggested_rewrite": suggested_rewrite,
  }

  # Store in DB or Fallback Memory list
  if db_connected:
    try:
      audit_collection.insert_one(audit_entry.copy())
    except Exception:
      fallback_audit_logs.append(audit_entry)
  else:
    fallback_audit_logs.append(audit_entry)

  return jsonify({
      "score": score,
      "violations": violations,
      "suggested_rewrite": suggested_rewrite,
      "role": role,
  })


@app.route("/api/v1/webhook-audit", methods=["POST"])
def webhook_audit():
  """API Gateway Webhook for external CMS and browser extensions."""
  auth_header = request.headers.get("Authorization")
  if not auth_header or "Bearer" not in auth_header:
    return jsonify({"error": "Unauthorized webhook request"}), 401

  data = request.get_json() or {}
  text = data.get("text", "")
  if not text:
    return jsonify({"error": "No text provided"}), 400

  violations = []
  for word in BANNED_WORDS:
    pattern = r"\b" + re.escape(word) + r"\b"
    if re.search(pattern, text, re.IGNORECASE):
      violations.append(f'"{word}": Prohibited claim.')

  score = max(20, 100 - (len(violations) * 20))
  if not violations:
    score = 100

  return jsonify({
      "status": "success",
      "score": score,
      "compliant": score >= 80,
      "violations_detected": len(violations),
  })


@app.route("/api/export-audit", methods=["GET"])
def export_audit():
  logs = []
  if db_connected:
    try:
      logs = list(audit_collection.find({}, {"_id": 0}))
    except Exception:
      logs = fallback_audit_logs
  else:
    logs = fallback_audit_logs

  report = {
      "project": "BrandGuard-AI",
      "team": "SOLOSYNTAX",
      "export_timestamp": datetime.now().isoformat(),
      "total_audits": len(logs),
      "audit_logs": logs,
  }
  return jsonify(report)


if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=5000)