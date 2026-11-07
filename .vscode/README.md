# 🛡️ BrandGuard AI

> **Automated Brand Governance & Policy Checking Platform** built for seamless compliance management.

---

## 🚀 Overview
**BrandGuard AI** is an intelligent brand governance tool designed to help marketing and legal teams automatically audit content against predefined brand guidelines. By catching exaggerated claims, unverified comparisons, and compliance risks before publication, BrandGuard AI ensures brand safety and tone consistency.

---

## ✨ Key Features
* **Automated Compliance Auditing:** Instant analysis of marketing copy and social posts against custom brand rules.
* **Risk & Violation Detection:** Flags absolute claims, unverified comparative statements, and urgency pressure tactics.
* **Actionable Recommendations:** Provides precise corrective feedback and alternative phrasing suggestions.
* **Interactive Approval Workflow:** Clear review interface allowing team leads to **Approve Content** or **Request Revision**.

---

## 🛠️ Tech Stack
* **Backend:** Python, Flask, REST APIs
* **Frontend:** HTML5, Tailwind CSS, JavaScript (Fetch API)
* **Environment:** Local development server running via Flask

---

## ⚙️ Step-by-Step Installation & Setup

Follow these steps to run the project locally on your machine:

### 1. Clone or Open the Project
Open your project folder in your terminal or VS Code where `app.py` and the `templates/` folder are located.

### 2. Install Dependencies
Open your terminal (in VS Code) and install the required Python packages (Flask):
```bash
pip install -r requirements.txt
(If you don't have requirements.txt, you can manually install Flask using: pip install flask)

3. Run the Application
Start the local development server by executing app.py:

Bash
python app.py
You will see output similar to this in your terminal:

Plaintext
 * Serving Flask app 'app'
 * Running on [http://127.0.0.1:5000](http://127.0.0.1:5000) (Press CTRL+C to quit)
4. Access in Browser
Open your web browser (Chrome, Edge, etc.) and navigate to:

Plaintext
[http://127.0.0.1:5000](http://127.0.0.1:5000)
💡 How to Use
Enter or modify your Brand Guidelines / Rules in the top text box.

Paste your marketing copy, social media post, or advertisement draft into the Content to Check box.

Click "Check Content Against Guidelines" to generate the AI evaluation report.

Review the flagged violations and click either Approve Content or Request Revision.

🏆 Hackathon Demo Ready
Built as a robust, low-latency governance tool optimized for fast, reliable local demonstrations without external quota constraints.