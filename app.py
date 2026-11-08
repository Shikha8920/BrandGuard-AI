from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)

ABSOLUTE_RULES = [
    "100% guaranteed",
    "best in market",
    "guaranteed",
    "act now",
    "limited time only",
    "risk-free",
    "proven best"
]

REPLACEMENTS = {
    "100% guaranteed": "designed for high reliability",
    "best in market": "a leading choice in the industry",
    "guaranteed": "proven",
    "act now": "explore today",
    "limited time only": "available now",
    "risk-free": "secure",
    "proven best": "industry-recognized"
}

def check_rules(text):
    violations = []
    text_lower = text.lower()
    for rule in ABSOLUTE_RULES:
        if rule in text_lower:
            violations.append({
                'rule': rule,
                'message': f"Potential non-compliant or exaggerated claim detected: '{rule}'."
            })
    return violations

def calculate_tone_score(text, violation_count):
    base_score = 100
    penalty = 25
    score = base_score - (violation_count * penalty)
    return max(score, 0)

def generate_smart_fix(text):
    fixed_text = text
    suggestions = []
    
    for rule in ABSOLUTE_RULES:
        if rule in fixed_text.lower():
            good_phrase = REPLACEMENTS.get(rule, "reviewed phrase")
            pattern = re.compile(re.escape(rule), re.IGNORECASE)
            fixed_text = pattern.sub(good_phrase, fixed_text)
            suggestions.append(f"Replace '{rule}' with '{good_phrase}'")
            
    return fixed_text, suggestions

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check-brand', methods=['POST'])
def audit_copy():
    data = request.get_json()
    copy_text = data.get('text', '')
    
    if not copy_text:
        return jsonify({'error': 'No text provided'}), 400

    violations = check_rules(copy_text)
    violation_count = len(violations)
    
    tone_score = calculate_tone_score(copy_text, violation_count)
    fixed_text, suggestions = generate_smart_fix(copy_text)
    
    return jsonify({
        'violations': violations,
        'violation_count': violation_count,
        'tone_score': tone_score,
        'smart_fix': fixed_text,
        'suggestions': suggestions
    })

@app.route('/add-rule', methods=['POST'])
def add_rule():
    data = request.get_json()
    new_rule = data.get('rule', '').strip().lower()
    
    if new_rule and new_rule not in ABSOLUTE_RULES:
        ABSOLUTE_RULES.append(new_rule)
        if new_rule not in REPLACEMENTS:
            REPLACEMENTS[new_rule] = "reviewed phrase"
        return jsonify({'success': True, 'message': f"Rule '{new_rule}' added successfully!", 'rules': ABSOLUTE_RULES})
    
    return jsonify({'success': False, 'message': 'Rule already exists or is empty.'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)