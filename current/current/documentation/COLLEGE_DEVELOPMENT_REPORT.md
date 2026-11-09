# AI Based Fake News Detection System
## Comprehensive College Project Development & Engineering Report

**Project Title:** Dual-Engine AI Based Fake News Detection System  
**Academic Degree:** Master of Computer Applications (MCA) / B.Tech Computer Science  
**Author / Developer:** College Project Team  
**Development Supervisor:** Academic Project Committee  
**Version:** 1.4.0 (Phases 1, 2, 3 & 4 Fully Completed)  
**Last Updated:** November 2026  

---

### Executive Summary

The **AI Based Fake News Detection System** is an end-to-end full-stack software application engineered to combat digital misinformation and deceptive claims across digital and print media formats. Unlike static machine learning proofs-of-concept, this platform implements a production-grade **dual-engine architecture** uniting:
1. **Linguistic Machine Learning Engine**: Low-latency, deterministic text classification utilizing sublinear TF-IDF $(1,2)$ n-gram feature representations and a Platt-calibrated Support Vector Machine (`CalibratedClassifierCV` wrapping `LinearSVC`).
2. **Generative LLM Fact-Checking Engine**: Real-time semantic and factual verification powered by Google Gemini (Gemini 2.5 Flash via official `google-genai` Python SDK).
3. **Automated Consensus Engine**: A reconciliation layer that determines whether the linguistic features and contextual fact-checking agree (`AGREE`, `DISAGREE`, `INCONCLUSIVE`).
4. **Relational Telemetry & Auditing**: 11 normalized database tables supporting user history, dataset versioning, model performance tracking, and administrative audit logging.

This development document serves as the formal engineering audit trail for academic evaluation, project defense (Viva Voce), and future project enhancement.

---

### 1. System Architecture & Engineering Stack

```text
                               +--------------------------------------------+
                               |         React 18.3 Web Client              |
                               |  - Citizen User Portal                     |
                               |  - Admin Dashboard & Analytics (Chart.js)  |
                               +---------------------+----------------------+
                                                     |
                                            REST API | (Axios / JSON)
                                                     v
                               +--------------------------------------------+
                               |          Flask 3.1 REST Backend            |
                               |  - JWT Authentication & RBAC               |
                               |  - Document Extraction (PDF, Word, CSV)    |
                               |  - Blueprint Modular Routing               |
                               +---------+------------------------+---------+
                                         |                        |
                   +---------------------+                        +---------------------+
                   v                                                                    v
+------------------------------------+                                +-----------------------------------+
|      Linguistic ML Engine          |                                |    Gemini LLM Fact Engine         |
|  - Sublinear TF-IDF (1,2) N-Grams  |                                |  - Gemini 2.5 Flash               |
|  - Platt-Calibrated Linear SVM     |                                |  - Strict Anti-Prompt Injection   |
|  - Sub-2ms Deterministic Inference |                                |  - Live Claim Plausibility        |
+------------------+-----------------+                                +-----------------+-----------------+
                   |                                                                    |
                   +---------------------+                        +---------------------+
                                         v                        v
                               +--------------------------------------------+
                               |             Consensus Engine               |
                               |   Reconciliation: AGREE / DISAGREE         |
                               +---------------------+----------------------+
                                                     |
                                                     v
                               +--------------------------------------------+
                               |     Relational Database (11 Tables)        |
                               |   - SQLite (Zero-Config Development)       |
                               |   - MySQL 8.0 (Enterprise Deployment)      |
                               +--------------------------------------------+
```

#### Technology Stack Specifications
- **Operating System Environment**: Windows 11
- **Host Python Environment**: Python 3.13.5 (`C:\Python313\python.exe`) - Local native installation preserved
- **Virtual Environment**: `.venv` (created via `python -m venv`)
- **Frontend Framework**: React.js 18.3.1 bootstrapped with Vite 6.0 (Port 5173)
- **UI & Visualization**: Bootstrap 5.3.3, Chart.js 4.4.7, React-Icons, React-Toastify
- **Backend Framework**: Python Flask 3.1.3 with Werkzeug 3.1.9 (Port 5000)
- **Database Layer**: SQLAlchemy 2.1.8 / Flask-SQLAlchemy 3.1.1 with PyMySQL 1.2.3 & SQLite connectors
- **Machine Learning**: Scikit-Learn 1.9.1, Pandas 3.1.1, NumPy 2.5.4, Joblib 1.6.0
- **Natural Language Processing**: NLTK 3.10.4 (Tokenization, Stopwords, Text Cleaning)
- **LLM SDK**: Official Google GenAI SDK (`google-genai` 3.0.0) with Gemini 2.5 Flash
- **Document Processing**: `pypdf` 7.0.0 for PDF extraction, `python-docx` 1.2.0 for MS Word documents
- **Automated Test Suite**: Pytest 9.2.0 (15 test cases)

---

### 2. Development Process & Milestones

#### Milestone 1: Architectural Audit & Diagnostic Phase (Completed)
- Located repository inside nested directory path `current/current/`.
- Identified broken legacy `.venv` tied to non-existent path `C:\Users\rohit\...\Python314\python.exe`.
- Discovered 160-item realistic dataset (`Self-generated.csv`) located at workspace root.
- Verified frontend build pipeline: Vite compiled cleanly in 2.05s.
- Confirmed relational schema: SQLite database (`backend/fake_news_dev.db`) pre-seeded with 11 tables.

#### Milestone 2: Environment Normalization (Phase 1 - COMPLETED)
- Strictly preserved user laptop's native Python installation (**Python 3.13.5**). No external Python version installed.
- Purged invalid legacy virtual environment and recreated `.venv` with `C:\Python313\python.exe -m venv current\current\.venv`.
- Installed all 19 project dependencies from `backend/requirements.txt` into the newly created virtual environment.
- Validated that all core modules import cleanly without conflict.
- Executed automated unit test suite (`pytest backend/tests -v`). **All 15 tests passed with 100% success rate**.

#### Milestone 3: Dataset Harmonization & 500-Record Expansion (Phase 2 - COMPLETED)
- Developed automated combinatorial synthesis pipeline (`scripts/generate_500_records.py`).
- Synthesized **500 guaranteed-unique records** (250 Real and 250 Fake) across 8 distinct domains.
- Appended records to `Self-generated.csv` (total: **660 records: 331 Real, 329 Fake**).
- Implemented `scripts/sync_self_dataset.py` mapping all 660 records to canonical schema in `dataset/self_generated/self_generated_news.csv`.
- Executed `scripts/create_hybrid_dataset.py`, harmonizing self-generated data with Kaggle benchmark data:
  - **Total Harmonized Hybrid Dataset:** **684 records**
  - **Class Balance:** **343 REAL (50.15%) vs 341 FAKE (49.85%)**
  - **Deduplication Rate:** Zero dropped records (100% unique cryptographic hashes).
- Validated datasets using `scripts/validate_datasets.py`: 0 nulls, 0 duplicates, valid binary labels.
- Updated SQLite relational database telemetry (`datasets` table) to reflect version `v2.0.0`.
- Re-ran Pytest suite: **15/15 unit tests passed**.

#### Milestone 4: Model Retraining, Calibration & Benchmarking (Phase 3 - COMPLETED)
- Retrained feature extraction pipeline: TF-IDF Vectorizer with unigrams & bigrams $(1,2)$, sublinear term scaling, yielding **5,000 features**.
- Evaluated two candidate classification pipelines on an 80/20 stratified split (547 training / 137 testing samples):
  1. **Candidate 1: Logistic Regression (L2 regularization, liblinear solver)**
  2. **Candidate 2: Calibrated Linear SVM (`CalibratedClassifierCV` with 3-fold Platt Sigmoidal Scaling)**
- Selected **Champion Model**: Calibrated Linear Support Vector Machine (**Accuracy: 98.54%, Macro F1: 0.9854, ROC-AUC: 1.0000**).
- Re-serialized artifacts natively with Scikit-Learn 1.9.1 on Python 3.13.5 (`trained_models/fake_news_model.pkl`, `tfidf_vectorizer.pkl`, `model_metadata.json`), completely eliminating library version warnings.
- Registered model version `v2.0.0` as `is_active = True` in SQLite database `model_versions` table.
- Updated academic conference draft (`research_paper/experimental_results.md`).

#### Milestone 5: Full-Stack Integration, Live Verification & Telemetry (Phase 4 - COMPLETED)
- Identified and fixed Windows SQLite path formatting in `backend/config.py` by converting backslashes to forward-slashes (`sqlite:///F:/Fake news detection/...`), preventing URI parsing errors.
- Bootstrapped and seeded all 11 database tables in SQLite developer database.
- Started Flask REST API daemon server on `http://127.0.0.1:5000`.
- Started Vite React web application on `http://localhost:5173`.
- Tested and verified complete user interaction flows via Headless Chrome:
  - **Citizen User Authentication**: Login (`user@fakenews.ai`), profile session, and JWT token issuance.
  - **Live Linguistic Inference**: Tested real-time detection on both real (98.99% confidence) and fake claims (98.81% confidence).
  - **Explainability**: Salient signal terms dynamically extracted and displayed with probability breakdowns.
  - **Bookmarking & Saved News**: Verified bookmark insertion and retrieval in `saved_news` table.
  - **Admin Governance Portal**: Verified dashboard telemetry KPIs, dataset validation modal, model retraining specifications, and administrative audit trails.

---

### 3. Empirical Model Performance & Comparison (Phase 3 Results)

| Metric | Version 1.0.0 (72 Records) | Version 2.0.0 (684 Records) - LR | Version 2.0.0 (684 Records) - Calibrated Linear SVM (Champion) |
| :--- | :--- | :--- | :--- |
| **Accuracy** | 93.33% | 98.54% | **98.54%** |
| **F1 Score (Macro)** | 0.9321 | 0.9854 | **0.9854** |
| **F1 Score (Real Class)** | 0.9231 | 0.9857 | **0.9857** |
| **ROC-AUC Score** | 0.9643 | 1.0000 | **1.0000** |
| **Real Class Recall** | 85.71% | 100.0% | **100.0%** (Zero False Negatives) |
| **Fake Class Precision** | 88.89% | 100.0% | **100.0%** (Zero Authentic News Misclassified) |
| **Confusion Matrix (Test)** | $\begin{bmatrix} 8 & 0 \\ 1 & 6 \end{bmatrix}$ | $\begin{bmatrix} 66 & 2 \\ 0 & 69 \end{bmatrix}$ | $\begin{bmatrix} 66 & 2 \\ 0 & 69 \end{bmatrix}$ |
| **Training Corpus Size** | 57 samples | 547 samples | **547 samples** |
| **Holdout Test Size** | 15 samples | 137 samples | **137 samples** |
| **Feature Dimensions** | 3,182 | 5,000 | **5,000** |

---

### 4. Technical Problems Resolved During Development

| Issue / Bug | Root Cause | Engineering Resolution |
|---|---|---|
| **Invalid Python Interpreter Path** | Legacy `.venv` hardcoded to external path `C:\Users\rohit\...\Python314\python.exe`. | Purged invalid directory and generated a fresh `.venv` utilizing native `C:\Python313\python.exe`. |
| **Pytest Import Path Failure** | System PYTHONPATH omitted parent project root when tests ran from different directories. | Set execution directory context to project root `current/current` and configured standard import paths. |
| **Small Dataset Sample Size** | Initial training set used only 72 rows, causing risk of over-fitting. | Synthesized 500 new diverse records and integrated root data, expanding hybrid corpus to 684 records. |
| **Inconsistent Version Warning** | Artifacts serialized with Scikit-Learn 1.9.0 gave runtime warnings on 1.9.1. | Retrained and re-serialized model natively with Scikit-Learn 1.9.1 on Python 3.13.5. |
| **Windows SQLite URI Path Syntax** | `os.path.join` created Windows backslashes `\`, causing SQLAlchemy URI parser failure (`\F` escape error). | Converted backslashes to standard forward-slashes in `backend/config.py` (`sqlite:///F:/Fake news detection/...`). |

---

### 5. Test Suite Execution Results (Phase 4 Verification)

Test Suite: `pytest backend/tests -v`  
Environment: `Python 3.13.5 (win32)`  
Result: **15 Passed, 0 Failed (100% Pass Rate)**

| Test File | Test Case | Status | Verified Functionality |
|---|---|---|---|
| `test_auth.py` | `test_user_registration_success` | **PASSED** | Citizen user registration, password hashing |
| `test_auth.py` | `test_user_registration_duplicate_email` | **PASSED** | Rejection of duplicate email addresses |
| `test_auth.py` | `test_user_login_success` | **PASSED** | JWT token generation and credential verification |
| `test_auth.py` | `test_admin_registration_rejects_without_secret` | **PASSED** | Admin endpoint rejection without passcode |
| `test_auth.py` | `test_admin_registration_success_with_valid_secret`| **PASSED** | Admin privilege escalation with valid key |
| `test_dataset_validation.py` | `test_validate_self_generated_dataset` | **PASSED** | Integrity of expanded 660 self-generated records |
| `test_dataset_validation.py` | `test_validate_hybrid_dataset` | **PASSED** | Integrity of expanded 684 hybrid records |
| `test_file_parser.py` | `test_extract_text_txt` | **PASSED** | Raw text file extraction |
| `test_file_parser.py` | `test_process_csv_batch` | **PASSED** | CSV batch row ingestion and column mapping |
| `test_file_parser.py` | `test_reject_unsupported_extensions` | **PASSED** | Security filter against unauthorized file types |
| `test_gemini_service.py` | `test_gemini_unconfigured_offline_degradation` | **PASSED** | Graceful degradation when API key is unconfigured |
| `test_ml_pipeline.py` | `test_clean_text_removes_stopwords_and_urls` | **PASSED** | NLP preprocessing, URL stripping, stopwords |
| `test_ml_pipeline.py` | `test_combine_title_and_article_weighting` | **PASSED** | Headline-to-body text weighting |
| `test_ml_pipeline.py` | `test_prediction_service_inference_bounds` | **PASSED** | Confidence scores strictly bounded in $[0.0, 1.0]$ |
| `test_ml_pipeline.py` | `test_prediction_hash_determinism` | **PASSED** | SHA-256 deduplication and cache determinism |

---

*This report is maintained continuously throughout the development lifecycle for college project presentation, thesis documentation, and Viva Voce examination.*
