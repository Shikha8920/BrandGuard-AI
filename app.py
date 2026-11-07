from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check-brand', methods=['POST'])
def analyze():
    data = request.get_json() or {}
    content = data.get('content', 'Sample Content')
    
    report = """### BrandGuard AI Evaluation Report

**Status:** ⚠️ **Flagged for Guideline Violations**

**Key Violations Detected:**
1. **Exaggerated & Absolute Claims:** 
   - *Issue:* Unsubstantiated absolute phrases found.
   - *Recommendation:* Use objective, verifiable language.
2. **Compliance Check:** 
   - *Recommendation:* Remove guarantees and add appropriate disclaimers before publishing."""

    return jsonify({
        "success": True,
        "analysis": report
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)