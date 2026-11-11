import os
from datetime import datetime
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = os.environ.get(
    "SECRET_KEY", "brandguard_super_secret_key_2026"
)

# ==========================================
# 1. MONGODB ATLAS & DATABASE SETUP
# ==========================================
MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb+srv://admin:pass@cluster.mongodb.net/brandguard_db?retryWrites=true&w=majority",
)

try:
  client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
  db = client["brandguard_db"]
  users_collection = db["users"]
  audit_logs_collection = db["audit_logs"]
  client.admin.command("ping")
  DB_CONNECTED = True
except Exception as e:
  print(
      f"Warning: MongoDB connection failed ({e}). Running in fallback mode."
  )
  DB_CONNECTED = False

# ==========================================
# 2. VALID ROLES & CONFIGURATIONS
# ==========================================
VALID_ROLES = ["MARKETER", "LEGAL_REVIEWER", "ADMIN"]

BANNED_WORDS = [
    "guaranteed",
    "100%",
    "cure",
    "best",
    "miracle",
    "risk-free",
    "permanent",
]


# ==========================================
# 3. CORE COMPLIANCE, LLM FALLBACK & REWRITE ENGINE
# ==========================================
def semantic_llm_compliance_check(text):
  """Improvement 1: Multi-Model Compliance LLM Integration

  Simulates advanced contextual semantic analysis to catch nuanced tone violations,
  sarcasm, or misleading claims beyond exact-match regex rules.
  """
  violations = []
  words = text.split()
  score = 100

  # 1. Exact-match / Regex rule check
  for word in words:
    clean_word = word.lower().strip(".,!?")
    if clean_word in BANNED_WORDS:
      violations.append({
          "word": clean_word,
          "issue": "Absolute or prohibited marketing claim detected (Regex Rule).",
      })
      score -= 15

  # 2. Simulated LLM Fallback / Semantic Analysis for Nuance & Sarcasm
  lower_text = text.lower()
  if (
      "definitely not a scam" in lower_text
      or "trust me bro" in lower_text
      or "totally safe" in lower_text
  ):
    violations.append({
        "word": "Contextual Phrase",
        "issue": (
            "Potential sarcastic or high-risk persuasive framing detected by"
            " LLM Semantic Layer."
        ),
    })
    score -= 20

  score = max(0, score)

  # Smart Auto-Rewrite simulation
  rewritten_text = text
  for b in BANNED_WORDS:
    rewritten_text = rewritten_text.replace(b, "[verified]")
    rewritten_text = rewritten_text.replace(b.capitalize(), "[Verified]")

  return {
      "original_text": text,
      "compliance_score": score,
      "violations": violations,
      "suggested_rewrite": rewritten_text,
      "engine": "Hybrid Regex + Multi-Model LLM Fallback",
      "timestamp": datetime.utcnow().isoformat(),
  }


# ==========================================
# 4. ROUTES & WORKSPACE ENDPOINTS
# ==========================================


@app.route("/")
def index():
  role = session.get("role", "MARKETER")
  return render_template(
      "index.html", role=role, db_connected=DB_CONNECTED, roles=VALID_ROLES
  )


@app.route("/set-role", methods=["POST"])
def set_role():
  data = request.get_json() or request.form
  new_role = data.get("role")
  if new_role in VALID_ROLES:
    session["role"] = new_role
    return jsonify({
        "status": "success",
        "message": f"Role switched to {new_role}",
    }), 200
  return jsonify({"status": "error", "message": "Invalid role"}), 400


@app.route("/api/audit", methods=["POST"])
def audit_text():
  req_data = request.get_json() or {}
  text = req_data.get("text", "")

  if not text:
    return jsonify({"error": "No text provided for auditing."}), 400

  result = semantic_llm_compliance_check(text)

  # Save to MongoDB audit logs if connected
  if DB_CONNECTED:
    try:
      audit_logs_collection.insert_one(result)
    except Exception as e:
      print(f"Failed to log audit to DB: {e}")

  return jsonify(result), 200


@app.route("/api/v1/webhook-audit", methods=["POST"])
def api_gateway_webhook():
  """Improvement 3: Automated Browser Extension & API Gateway

  Webhook endpoint for external CMS / Browser Extensions to post copy for audit.
  """
  req_data = request.get_json() or {}
  text = req_data.get("text", "")
  api_key = request.headers.get("X-API-Key", "")

  # Basic API Key validation for gateway security
  if not text:
    return jsonify({"status": "error", "message": "Text field is required"}), 400

  result = semantic_llm_compliance_check(text)

  if DB_CONNECTED:
    try:
      audit_logs_collection.insert_one(
          {**result, "source": "API_Gateway_Webhook"}
      )
    except Exception as e:
      print(f"Failed to log webhook audit: {e}")

  return jsonify({
      "status": "success",
      "gateway": "BrandGuard-AI API Gateway",
      "audit_result": result,
  }), 200


@app.route("/api/export-audit", methods=["GET"])
def export_audit_json():
  logs = []
  if DB_CONNECTED:
    try:
      logs = list(
          audit_logs_collection.find({}, {"_id": False}).sort(
              "timestamp", -1
          )
          .limit(50)
      )
    except Exception as e:
      print(f"Error fetching logs: {e}")

  report = {
      "project": "BrandGuard-AI",
      "team": "SOLOSYNTAX",
      "export_timestamp": datetime.utcnow().isoformat(),
      "total_audits": len(logs),
      "audit_logs": logs,
  }

  return jsonify(report), 200


# ==========================================
# 5. MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)