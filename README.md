# BrandGuard AI 🛡️
### Enterprise Compliance Governance Engine | CodeTitans India 2026 (Round 3)

**Team:** SOLOSYNTAX  
**Team Leader:** Shikha Chaurasia  

---

## 🌟 Overview
**BrandGuard AI** is an advanced, enterprise-grade compliance governance and automated brand tone enforcement platform. Designed for modern marketing teams, agencies, and legal departments, it ensures that all outgoing public copy strictly adheres to brand guidelines, regulatory standards, and tone consistency metrics in real-time through a hybrid rule-engine and semantic LLM fallback layer.

---

## 🚀 Key Enterprise Features & Round 3 Improvements

1. **Multi-Model Compliance LLM Integration (Improvement 1)**
   - Combines exact-match regex rules with an advanced semantic analysis fallback layer.
   - Detects nuanced tone violations, sarcastic framing, and high-risk persuasive phrasing beyond simple keyword matching.

2. **Role-Based Enterprise Workspace & Audit Dashboards (Improvement 2)**
   - Secure session and user role management supporting distinct enterprise workflows (`MARKETER`, `LEGAL_REVIEWER`, `ADMIN`).
   - Persistent historical audit logging backed by **MongoDB Atlas** cloud storage.

3. **Automated Multi-Platform Browser Extension & API Gateway (Improvement 3)**
   - Secure webhook API endpoint (`/api/v1/webhook-audit`) protected via request headers.
   - Enables browser extensions and external Content Management Systems (CMS) to scan live copy instantly before publishing.

4. **Automated Brand Tone Consistency Scoring (0–100 Scale)**
   - Evaluates marketing copy against pre-defined absolute rules and dynamic penalties.
   - Features real-time dynamic color-coded badges (Green for compliant, Yellow for moderate, Red for high risk).

5. **Smart Auto-Rewrite Engine & Audit Export**
   - Instantly suggests professional, compliant alternatives with bracketed verification.
   - Generates and downloads comprehensive compliance audit trails in JSON format (`brandguard_audit_report.json`) for legal archiving.

---

## 💻 Tech Stack

- **Backend:** Python, Flask REST API, Gunicorn (`app.py`)
- **Database:** MongoDB Atlas (Cloud Persistent Storage with fallback mode)
- **Frontend:** HTML5, Tailwind CSS, JavaScript (AJAX / Fetch API)
- **Environment:** Windows OS, VS Code, Render Cloud

---

## 🔌 API Endpoints Reference

| Endpoint | Method | Description |
| :--- | :---: | :--- |
| `/` | `GET` | Enterprise workspace dashboard (Role switcher view) |
| `/set-role` | `POST` | Switches active user role (`MARKETER`, `LEGAL_REVIEWER`, `ADMIN`) |
| `/api/audit` | `POST` | Runs hybrid compliance scan on input marketing text |
| `/api/v1/webhook-audit` | `POST` | External CMS / Browser extension API gateway hook |
| `/api/export-audit` | `GET` | Exports complete historical audit reports in structured JSON |

---

## ⚙️ Installation & Local Setup

Follow these steps to run BrandGuard AI locally on your machine:

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/Shikha8920/BrandGuard-AI.git](https://github.com/Shikha8920/BrandGuard-AI.git)
   cd BrandGuard-AI
Install Dependencies:
Make sure Python is installed, then install required packages:

Bash
pip install flask pymongo gunicorn dnspython
Run the Application:

Bash
python app.py
Access the Dashboard:
Open your browser and navigate to:http://127.0.0.1:5000/

🧪 Testing the Workflow
Test Copy 1 (High Violations & Sarcasm/Absolute Claims Test):

"Get our cheapest 100% guaranteed product today! Hurry, massive discount available for a limited time only. It is the best in market and risk-free. Trust me bro, definitely not a scam."

Test Copy 2 (Clean & Compliant Copy):

"Explore our secure enterprise solution designed for high reliability and industry-recognized performance. Available now for your team."

📜 License
Developed with 💻 by Team SOLOSYNTAX for CodeTitans India 2026.