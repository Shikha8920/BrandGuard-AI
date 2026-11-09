import os
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Initial default compliance rules and banned phrases mapping
# (Phrase to check: [Penalty score, Suggested alternative])
COMPLIANCE_RULES = {
    "guaranteed": {
        "penalty": 25,
        "alternative": "industry-standard / proven",
    },
    "100%": {"penalty": 30, "alternative": "highly reliable"},
    "best": {"penalty": 15, "alternative": "top-tier / leading"},
    "cheap": {"penalty": 20, "alternative": "cost-effective / economical"},
    "free": {"penalty": 10, "alternative": "complimentary"},
}


@app.route("/")
def index():
  return render_template("index.html", rules=COMPLIANCE_RULES)


@app.route("/analyze", methods=["POST"])
def analyze_text():
  data = request.get_json()
  text = data.get("text", "")

  if not text:
    return jsonify({"error": "No text provided for analysis"}), 400

  score = 100
  violations_found = []
  rewritten_text = text

  # Check text against rules (case-insensitive simulation)
  lower_text = text.lower()
  for phrase, rule_info in COMPLIANCE_RULES.items():
    if phrase in lower_text:
      score -= rule_info["penalty"]
      violations_found.append({
          "matched_phrase": phrase,
          "penalty": rule_info["penalty"],
          "alternative": rule_info["alternative"],
      })
      # Simple replacement for auto-rewrite
      rewritten_text = (
          rewritten_text.replace(phrase, rule_info["alternative"])
          .replace(phrase.capitalize(), rule_info["alternative"].capitalize())
      )

  # Ensure score doesn't drop below 0
  score = max(0, score)

  # Risk categorization
  if score >= 90:
    risk_level = "Low Risk (Compliant)"
  elif score >= 70:
    risk_level = "Medium Risk (Review Recommended)"
  else:
    risk_level = "High Risk (Non-Compliant)"

  return jsonify({
      "original_text": text,
      "rewritten_text": rewritten_text,
      "compliance_score": score,
      "risk_level": risk_level,
      "violations": violations_found,
  })


@app.route("/add-rule", methods=["POST"])
def add_rule():
  data = request.get_json()
  phrase = data.get("phrase", "").strip().lower()
  penalty = data.get("penalty", 20)
  alternative = data.get("alternative", "").strip()

  # Fallback if only phrase is provided from frontend UI
  if not alternative:
    alternative = "approved standard term"

  if not phrase:
    return jsonify({"error": "Phrase is required"}), 400

  COMPLIANCE_RULES[phrase] = {"penalty": int(penalty), "alternative": alternative}
  return jsonify({
      "message": f"Rule for '{phrase}' added successfully",
      "rules": COMPLIANCE_RULES,
  })


@app.route("/export-audit", methods=["POST"])
def export_audit():
  data = request.get_json()
  audit_trail = {
      "audit_timestamp": "2026-11-09",
      "status": "Generated",
      "analyzed_data": data,
  }
  return jsonify(audit_trail)


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)