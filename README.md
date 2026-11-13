# BrandGuard-AI 🛡️
> Enterprise Compliance Governance & AI-Driven Content Auditing Platform  
> **Event:** CodeTitans India 2026 | **Team:** SOLOSYNTAX  
> **Team Leader:** Shikha Chaurasia  
> **Repository:** [https://github.com/Shikha8920/BrandGuard-AI](https://github.com/Shikha8920/BrandGuard-AI)  
> **Live Application URL:** [https://brandguard-ai-h7xf.onrender.com/](https://brandguard-ai-h7xf.onrender.com/) *(Note: Hosted on Render cloud tier; please allow 30–50 seconds for initial spin-up from sleep mode if inactive).*

---

## 📋 Table of Contents
1. Overview
2. Key Improvements in Final Round (vs. Round 2)
3. Architecture & Core Features
4. API Endpoints & Documentation
5. Project Directory Structure
6. Local Installation & Setup Guide
7. Comprehensive Benchmark Testing Results
8. Team & Submission Details

---

## 🚀 1. Overview
BrandGuard-AI is an enterprise-grade compliance governance platform built to automate marketing copy auditing across digital channels. It protects brands from regulatory penalties by detecting absolute claims, prohibited health/financial guarantees, and manipulative or sarcastic framing in real-time.

---

## ⚡ 2. Key Improvements in Final Round (vs. Round 2)
1. **Strict Whole-Word Boundary Regex Engine (`\b`):** Upgraded string matching logic using `re.escape()` and strict word boundaries (`\b`) to completely eliminate substring bugs (e.g., ensuring words like "secure" remain safe).
2. **Multi-Model LLM Semantic Fallback Layer:** Detects implicit persuasive framing, sarcasm, and high-risk tonal violations (such as "trust me bro" or "definitely not a scam").
3. **Enterprise JSON Audit Archiving & Export (`/api/export-audit`):** Implemented a dedicated secure audit logging endpoint tracking timestamps, active roles (`MARKETER`, `LEGAL_REVIEWER`, `ADMIN`), and automated smart rewrites, backed by MongoDB Atlas cloud persistence and automated in-memory redundancy.

---

## 🛠️ 3. Architecture & Core Features
* **Role-Based Access Control (RBAC):** Dynamic role switcher banner (`MARKETER`, `LEGAL_REVIEWER`, `ADMIN`) enabling judges to instantly test permission strictness levels.
* **Live Compliance Dashboard:** Real-time scoring system (0–100 scale) with dynamic color-coded badges and instant inline text sanitization (`[verified]`).
* **Resilient Storage Architecture:** MongoDB Atlas cloud integration paired with an intelligent in-memory fallback mechanism (`fallback_audit_logs`).

---

## 🔌 4. API Endpoints & Documentation
* **`POST /api/audit`:** Audits marketing copy against regex rules and semantic checks.
* **`POST /api/v1/webhook-audit`:** Secure API Gateway webhook for external CMS/extensions.
* **`GET /api/export-audit`:** Exports full audit logs in structured JSON format.
* **`POST /set-role`:** Updates active workspace role session.

---

## 📂 5. Project Directory Structure
```text
BrandGuard-AI/
├── templates/
│   └── index.html         # Frontend UI with Role Switcher & Live Auditing
├── .env                   # Environment configuration (Secret keys & Mongo URI)
├── app.py                 # Core Flask backend application & audit engines
├── Procfile               # Production WSGI process configuration
├── requirements.txt       # Python dependencies (Flask, Gunicorn, PyMongo, etc.)
└── README.md              # Comprehensive project documentation
```

---

## 💻 6. Local Installation & Setup Guide
**Clone the Repository:**

Bash
git clone [https://github.com/Shikha8920/BrandGuard-AI.git](https://github.com/Shikha8920/BrandGuard-AI.git)
cd BrandGuard-AI
Install Dependencies:

Bash
pip install -r requirements.txt
Configure Environment Variables:
Create a .env file in the root directory:

Code snippet
MONGO_URI=your_mongodb_atlas_connection_string
SECRET_KEY=your_secure_flask_secret_key
Run the Flask Development Server:

Bash
python app.py
Access the Application:
Open your browser and navigate to: http://127.0.0.1:5000

---

## 📊 7. Comprehensive Benchmark Testing Results
* **High Violation & Sarcasm:** Score 20/100, 6 violations detected (Regex + Sarcasm).
* **Medical / Absolute Claims:** Score 40/100, 4 prohibited medical claims flagged.
* **Clean Enterprise Copy:** Score 100/100, 0 violations (\b word boundary verified for secure).

---

## 🏆 8. Team & Submission Details
* **Hackathon: CodeTitans India 2026**
* **Team Name: SOLOSYNTAX**
* **Team Leader: Shikha Chaurasia**
* **Live Cloud Deployment: https://brandguard-ai-h7xf.onrender.com/**

---