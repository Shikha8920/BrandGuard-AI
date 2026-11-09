import os
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Initial compliance rules mapping
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
  return render_template("index.html")


@app.route("/check-brand", methods=["POST"])
def check_brand():
  data = request.get_json()
  text = data.get("text", "")

  if not text:
    return jsonify({"error": "No text provided"}), 400

  score = 100
  violations_found = []
  smart_fix_text = text

  lower_text = text.lower()
  for phrase, rule_info in COMPLIANCE_RULES.items():
    if phrase in lower_text:
      score -= rule_info["penalty"]
      violations_found.append({
          "rule": phrase.upper(),
          "message": (
              f"Detected banned/restricted term '{phrase}'. Recommended"
              f" alternative: '{rule_info['alternative']}'."
          ),
      })
      smart_fix_text = (
          smart_fix_text.replace(phrase, rule_info["alternative"])
          .replace(phrase.capitalize(), rule_info["alternative"].capitalize())
      )

  score = max(0, score)

  suggestions = [
      "Ensure all marketing claims are backed by verifiable data.",
      (
          "Maintain a professional and customer-centric tone across all ad"
          " copies."
      ),
      "Review custom brand guidelines regularly for policy compliance.",
  ]

  return jsonify({
      "tone_score": score,
      "violations": violations_found,
      "smart_fix": smart_fix_text,
      "suggestions": suggestions,
  })


@app.route("/add-rule", methods=["POST"])
def add_rule():
  data = request.get_json()
  # Frontend sends 'rule', backend captures it safely
  phrase = data.get("rule") or data.get("phrase", "")
  phrase = phrase.strip().lower()

  if not phrase:
    return jsonify({"success": False, "message": "Rule phrase is required"})

  penalty = int(data.get("penalty", 20))
  alternative = data.get("alternative", "").strip()
  if not alternative:
    alternative = "approved standard term"

  COMPLIANCE_RULES[phrase] = {"penalty": penalty, "alternative": alternative}

  return jsonify({
      "success": True,
      "message": f"Rule for '{phrase}' added successfully!",
      "rules": COMPLIANCE_RULES,
  })


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)