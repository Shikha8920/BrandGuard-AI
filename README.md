# BrandGuard-AI 🛡️
### Enterprise Compliance Governance & AI-Driven Content Auditing Platform
**CodeTitans India 2026 | Team SOLOSYNTAX**
* **Team Leader:** Shikha Chaurasia
* **Repository:** https://github.com/Shikha8920/BrandGuard-AI
---

## 📋 Table of Contents
1. [Overview](#-overview)
2. [Key Improvements in Final Round (vs. Round 2)](#-key-improvements-in-final-round-vs-round-2)
3. [Architecture & Core Features](#-architecture--core-features)
4. [API Endpoints & Documentation](#-api-endpoints--documentation)
5. [Project Directory Structure](#-project-directory-structure)
6. [Local Installation & Setup Guide](#-local-installation--setup-guide)
7. [Comprehensive Benchmark Testing Results](#-benchmark-testing-results)
8. [Team & Submission Details](#-team--submission-details)

---

## 🚀 Overview
**BrandGuard-AI** is an enterprise-grade compliance governance platform built to automate marketing copy auditing across digital channels. It protects brands from regulatory penalties by detecting absolute claims, prohibited health/financial guarantees, and manipulative or sarcastic framing.

---

## ⚡ Key Improvements in Final Round (vs. Round 2)
1. **Strict Whole-Word Boundary Regex Engine (`\b`):** Upgraded string matching logic using `re.escape()` and strict word boundaries (`\b`) to completely eliminate substring bugs (e.g., ensuring words like `secure` remain safe).
2. **Multi-Model LLM Semantic Fallback Layer:** Detects implicit persuasive framing, sarcasm, and high-risk tonal violations (such as `"trust me bro"` or `"definitely not a scam"`).
3. **Enterprise JSON Audit Archiving & Export (`/api/export-audit`):** Implemented a dedicated secure audit logging endpoint tracking timestamps, active roles (`MARKETER`, `LEGAL_REVIEWER`, `ADMIN`), and automated smart rewrites.

---

## 🛠️ Architecture & Core Features
* **Role-Based Access Control (RBAC):** Dynamic role switcher for `MARKETER`, `LEGAL_REVIEWER`, and `ADMIN`.
* **Live Compliance Dashboard:** Real-time scoring system (0–100 scale) with dynamic color-coded badges.
* **Resilient Storage Architecture:** MongoDB Atlas integration with an intelligent in-memory fallback mechanism (`fallback_audit_logs`).

---

## 🔌 API Endpoints
* **`POST /api/audit`** - Audits marketing copy against regex rules and semantic checks.
* **`POST /api/v1/webhook-audit`** - Secure API Gateway webhook for external CMS/extensions.
* **`GET /api/export-audit`** - Exports full audit logs in structured JSON format.
* **`POST /set-role`** - Updates active workspace role session.

---

## 💻 Local Installation & Setup Guide
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Shikha8920/BrandGuard-AI.git
   cd BrandGuard-AI

```

2. **Install Dependencies:**
```bash
pip install -r requirements.txt

```


3. **Run the Flask Development Server:**
```bash
python app.py

```


4. **Access the Application:**
Open your browser and navigate to: `[http://127.0.0.1:5000](http://127.0.0.1:5000)`

---

## 📊 Benchmark Testing Results

* **High Violation & Sarcasm:** Score **20/100**, 6 violations detected (Regex + Sarcasm).
* **Medical / Absolute Claims:** Score **40/100**, 4 prohibited medical claims flagged.
* **Clean Enterprise Copy:** Score **100/100**, 0 violations (`\b` word boundary verified for `secure`).

---

## 🏆 Team & Submission Details

* **Hackathon:** CodeTitans India 2026
* **Team Name:** SOLOSYNTAX
* **Team Leader:** Shikha Chaurasia

