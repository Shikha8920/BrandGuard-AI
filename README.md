# BrandGuard AI 🛡️
### Enterprise Compliance Governance Engine | CodeTitans India 2026 (Round 2)

**Team:** SOLOSYNTAX  
**Team Leader:** Shikha Chaurasia  

---

## 🌟 Overview
**BrandGuard AI** is an advanced, enterprise-grade compliance governance and automated brand tone enforcement platform. Designed for modern marketing teams, agencies, and legal departments, it ensures that all outgoing public copy strictly adheres to brand guidelines, regulatory standards, and tone consistency metrics in real-time.

---

## 🚀 Key Enterprise Features

1. **Automated Brand Tone Consistency Scoring (0–100 Scale)**
   - Evaluates marketing copy against pre-defined absolute rules and dynamic penalties.
   - Features real-time dynamic color-coded badges (Green for compliant, Yellow for moderate, Red for high risk).

2. **Smart Auto-Rewrite Engine**
   - Utilizes regex-based case-insensitive phrasal mapping to automatically detect non-compliant claims and suggest professional, compliant alternatives.

3. **Live Custom Rule Injector**
   - Empowers users and compliance officers to inject custom banned words, phrases, or brand guidelines on the fly (`/add-rule` API endpoint) for runtime policy adaptation without restarting the core engine.

4. **Export Compliance Audit Report**
   - Generates and downloads comprehensive compliance audit trails in JSON format (`brandguard_audit_report.json`), capturing original texts, tone scores, violation counts, and specific rule triggers for legal archiving.

---

## 💻 Tech Stack

* **Backend:** Python, Flask REST API (`app.py`)
* **Frontend:** HTML5, Tailwind CSS, JavaScript (AJAX / Fetch API)
* **Environment:** Windows OS, VS Code

---

## ⚙️ Installation & Local Setup

Follow these steps to run BrandGuard AI locally on your machine:

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/Shikha8920/BrandGuard-AI.git](https://github.com/Shikha8920/BrandGuard-AI.git)
   cd BrandGuard-AI
Install Dependencies:
Make sure Python and Flask are installed, then install required packages:

Bash
pip install flask
Run the Application:

Bash
python app.py
Access the Dashboard:
Open your browser and navigate to:

Plaintext
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)
🧪 Testing the Workflow
Test Copy 1 (High Violations & Custom Rule Test):

"Get our cheapest 100% guaranteed product today! Hurry, massive discount available for a limited time only. It is the best in market and risk-free."

Test Copy 2 (Clean & Compliant Copy):

"Explore our secure enterprise solution designed for high reliability and industry-recognized performance. Available now for your team."

📜 License
Developed with 💻 by Team SOLOSYNTAX for CodeTitans India 2026.