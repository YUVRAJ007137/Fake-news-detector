# AI Based Fake News Detection System

[![Python](https://img.shields.io/badge/Python-3.12%20%7C%203.14-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18.3-61dafb.svg)](https://react.dev/)
[![Flask](https://img.shields.io/badge/Flask-3.1-black.svg)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.9-orange.svg)](https://scikit-learn.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-00758f.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-Academic-green.svg)]()

> **Master of Computer Applications (MCA) Final Year Project**  
> An intelligent, full-stack, dual-engine news verification platform that couples **Platt-Calibrated Linear SVMs** and **TF-IDF Feature Representations** with **Google Gemini LLM Claim Analysis** and **MySQL Relational Auditing**.

---

## 1. Project Overview

The **AI Based Fake News Detection System** is an enterprise-grade software application designed to detect, classify, and explain deceptive claims across digital media. It moves beyond static prototypes by offering:
1. **Deterministic Linguistic Classification**: Sub-2ms classical ML predictions using sublinear TF-IDF $(1, 2)$ n-grams and calibrated Linear SVMs.
2. **Real-Time Factual Verification**: Live claim evaluation against world events powered by the official `google-genai` Python SDK.
3. **Consensus Arbitration**: Reconciles dual-engine verdicts, outputting transparent `AGREE`, `DISAGREE`, or `INCONCLUSIVE` statuses.
4. **Multi-Format Document Ingestion**: Secure text extraction and batch inference for PDF, DOCX, TXT, and CSV datasets.
5. **Relational Telemetry**: 11 normalized MySQL tables tracking user history, model versions, candidate training runs, bookmarked articles, and administrator security logs.

---

## 2. Technology Stack

### Frontend
- **Framework**: React.js 18.3 with Vite 6
- **Styling**: Bootstrap 5.3 + Custom Navy & Light Accent Theme
- **Routing & State**: React Router DOM 6.28 + React Context API
- **Charts & Telemetry**: Chart.js 4.4 + React-Chartjs-2
- **Icons & Alerts**: React Icons (FontAwesome) + React Toastify

### Backend
- **Framework**: Python Flask 3.1
- **API Architecture**: Modular Blueprints (Auth, News, Files, Datasets, Models, Admin, Health)
- **Database ORM**: Flask-SQLAlchemy 3.1 + SQLAlchemy 2.0 (PyMySQL Connector)
- **Security & Tokens**: Flask-JWT-Extended + Werkzeug Password Hashing
- **Configuration**: Python Dotenv

### Machine Learning & NLP
- **Core Libraries**: Scikit-learn, Pandas, NumPy, Joblib
- **Feature Extraction**: TF-IDF Vectorizer (Unigrams & Bigrams, 5,000 Dimensions, Sublinear TF)
- **Algorithms**: Calibrated Linear Support Vector Machine (`CalibratedClassifierCV`) & Logistic Regression
- **Probability Calibration**: 3-Fold Cross-Validated Platt Sigmoidal Scaling

### LLM Intelligence
- **SDK**: Official `google-genai` Python SDK
- **Model**: Gemini 2.5 Flash
- **Defenses**: Strict untrusted-data prompts neutralizing prompt injection attacks

### Document Processing
- **PDF**: `pypdf`
- **Word**: `python-docx`
- **Text & CSV**: Standard Library + Pandas

---

## 3. Mandatory Directory Structure

```text
AI-Based-Fake-News-Detection-System/
├── frontend/                  # React.js + Vite Web Application
│   ├── src/
│   │   ├── components/        # Navbar, Footer, PredictionCard
│   │   ├── context/           # AuthContext (JWT & Role state)
│   │   ├── layouts/           # UserLayout, AdminLayout
│   │   ├── pages/
│   │   │   ├── auth/          # Login, Register, AdminLogin, AdminRegister
│   │   │   ├── user/          # UserDashboard, PreviousNews, LatestNews, FileUpload, etc.
│   │   │   └── admin/         # AdminDashboard, Users, Predictions, Datasets, Models, etc.
│   │   ├── services/          # api.js, authService, newsService, fileService, adminService
│   │   └── styles/            # Master index.css
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
├── backend/                   # Python Flask REST API Service
│   ├── app.py                 # Application factory and entrypoint
│   ├── config.py              # Centralized environment configuration
│   ├── models/                # 11 SQLAlchemy ORM models
│   ├── routes/                # 8 Flask Blueprints
│   ├── services/              # PredictionService, GeminiService, FileService
│   ├── ml/                    # preprocessor.py (NLP cleaning & stopwords)
│   ├── utils/                 # auth_utils.py (JWT decorators & password hashing)
│   ├── tests/                 # 15 automated Pytest unit tests
│   ├── requirements.txt
│   └── .env.example
├── database/                  # Relational Database Scripts
│   ├── schema.sql             # Complete DDL script for 11 MySQL tables
│   ├── seed.sql               # Seed data for admin, demo user, news, and datasets
│   ├── init_db.py             # Automated Python database bootstrapper
│   └── README.md
├── dataset/                   # Data Stores
│   ├── self_generated/        # self_generated_news.csv (48 balanced records)
│   ├── kaggle/                # kaggle_news.csv + DATASET_SOURCE.md (24 records)
│   ├── hybrid/                # hybrid_dataset.csv (72 harmonized records)
│   └── reports/               # Audit and validation reports
├── trained_models/            # Serialized ML Artifacts
│   ├── fake_news_model.pkl    # Serialized calibrated champion model
│   ├── tfidf_vectorizer.pkl   # Serialized fitted TF-IDF vectorizer
│   └── model_metadata.json    # Verified empirical metrics
├── documentation/             # Complete Academic Deliverables
│   ├── diagrams/              # Mermaid Architecture, ER, DFD Levels 0/1/2, Sequence, ML
│   ├── installation_guide.md  # Detailed setup instructions
│   ├── user_manual.md         # Citizen user guide
│   ├── admin_manual.md        # Administrator operations guide
│   ├── testing_report.md      # Pytest execution report (15 passed)
│   ├── project_report.md      # University project report format
│   └── viva_questions_answers.md # 50+ Viva Voce questions and answers
├── research_paper/            # Research Paper Deliverables
│   ├── research_paper_draft.md # Academic conference paper draft
│   ├── literature_review.md   # Prior research analysis
│   ├── references.md          # Genuine IEEE/ACM citations
│   └── experimental_results.md# Empirical quantitative results
├── scripts/                   # CLI Automation Scripts
│   ├── generate_self_dataset.py
│   ├── prepare_kaggle_dataset.py
│   ├── create_hybrid_dataset.py
│   ├── validate_datasets.py
│   ├── train_model.py
│   └── evaluate_model.py
├── .gitignore
├── .env.example
└── README.md
```

---

## 4. Quick Start: Windows Setup & Execution

### Step 1: Install Python Dependencies
```powershell
pip install -r backend/requirements.txt
```

### Step 2: Install Frontend Dependencies
```powershell
npm.cmd --prefix frontend install
```

### Step 3: Initialize Database
```powershell
python database/init_db.py
```
*(By default, uses the local SQLite fallback in `backend/fake_news_dev.db` so the app runs instantly out of the box. To connect to your running MySQL80 service, configure `DB_PASSWORD` in `backend/.env` and set `USE_SQLITE_FALLBACK=false`)*

### Step 4: Generate Datasets & Train Champion Model
```powershell
python scripts/generate_self_dataset.py
python scripts/prepare_kaggle_dataset.py
python scripts/create_hybrid_dataset.py
python scripts/validate_datasets.py
python scripts/train_model.py
```

### Step 5: Start the Flask Backend (Port 5000)
```powershell
python backend/app.py
```

### Step 6: Start the React Frontend (Port 5173)
```powershell
npm.cmd --prefix frontend run dev
```
Open **`http://localhost:5173`** in your browser.

---

## 5. Default Demonstration Credentials

| Role | Access URL | Email | Password | Secret Code |
| :--- | :--- | :--- | :--- | :--- |
| **Administrator** | `/admin/login` | `admin@fakenews.ai` | `Admin@12345` | - |
| **Citizen User** | `/login` | `user@fakenews.ai` | `User@12345` | - |
| **New Admin Enrollment** | `/admin/register` | *(Any valid email)* | *(Min 8 chars)* | `AdminSecretPasscode2025!` |

---

## 6. Empirical Results & Performance

| Metric | Logistic Regression | Calibrated Linear SVM (Champion) |
| :--- | :--- | :--- |
| **Accuracy** | 93.33% | **93.33%** |
| **F1 Score (Macro)** | 0.9321 | **0.9321** |
| **F1 Score (Real Class)**| 0.9231 | **0.9231** |
| **ROC-AUC Score** | 0.9643 | **0.9643** |
| **Precision on Real News**| 100.0% | **100.0%** (Zero False Positives) |
| **Confusion Matrix** | $\begin{bmatrix} 8 & 0 \\ 1 & 6 \end{bmatrix}$ | $\begin{bmatrix} 8 & 0 \\ 1 & 6 \end{bmatrix}$ |

---

## 7. Automated Testing

Run the test suite:
```powershell
pytest backend/tests -v
```
All **15 automated tests** pass cleanly with 100% success rate.

Verify frontend build:
```powershell
npm.cmd --prefix frontend run build
```

---

## 8. Epistemic Notice & Ethical Boundaries

The system evaluates linguistic patterns and cross-checks claims against LLM knowledge bases. It does **not** claim absolute philosophical certainty of truth. Outputs are clearly marked with calibrated confidence percentages to assist human editorial judgment.
