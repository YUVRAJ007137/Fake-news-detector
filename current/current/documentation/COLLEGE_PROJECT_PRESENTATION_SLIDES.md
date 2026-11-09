# AI Based Fake News Detection System
## Presentation Slides & Speaker Defense Script (12-Slide Deck)

**Academic Level:** MCA / B.Tech Computer Science Final Year Project  
**File Generated:** `Fake_News_Detection_Presentation.pptx` (16:9 Widescreen)  
**Location:** [`F:\Fake news detection\Fake_News_Detection_Presentation.pptx`](file:///F:/Fake%20news%20detection/Fake_News_Detection_Presentation.pptx)  

---

### Slide 1: Title Slide
- **Title:** AI-Based Fake News Detection System
- **Subtitle:** Dual-Engine Verification Platform Coupling Platt-Calibrated Linear SVMs & TF-IDF with Google Gemini 2.5 Flash Claim Analysis & Relational Auditing
- **Candidate Details:** Master of Computer Applications (MCA) / B.Tech Computer Science Final Year Project
- **Key Badges:** 98.54% Accuracy | Sub-2ms Latency | 11 Relational Tables | 684 Balanced Records
> **Speaker Notes:**  
> "Respected panel members and examiners, good morning. Today I am presenting our final year project: an 'AI-Based Fake News Detection System'. Unlike typical single-model prototypes, our project implements a production-grade dual-engine architecture combining deterministic linguistic machine learning with real-time generative fact-checking."

---

### Slide 2: Problem Statement & Motivation
- **The Information Crisis:** Proliferation of deceptive claims on social networks, messaging platforms, and digital news feeds.
- **Limitation 1 (Linguistic Blindspot):** Sophisticated disinformation is written in perfect journalistic prose. Classical ML looks only at vocabulary style, not ground truth, and is easily deceived.
- **Limitation 2 (LLM Cost & Latency):** Large Language Models (LLMs) verify facts but are slow (1.5–4s), expensive, vulnerable to prompt injection, and prone to hallucinations.
- **Our Solution:** A hybrid dual-engine architecture with consensus arbitration and enterprise telemetry.
> **Speaker Notes:**  
> "The fundamental problem with existing fake news detectors is that liars can write with impeccable grammar, while true breaking news can sound sensational. A linguistic model only knows how text is written, not whether it is true. Conversely, calling an LLM for every query is too slow and expensive. Our dual-engine system bridges this gap."

---

### Slide 3: Proposed Architecture & Information Flow
- **Client Layer:** React 18.3 + Vite 6 + Bootstrap 5.3 + Chart.js.
- **Backend API Layer:** Flask 3.1 with 8 Blueprints, JWT tokens, and SHA-256 deduplication caching.
- **Dual Intelligence Tier:**
  - *Engine 1 (Linguistic ML):* Preprocessor $\rightarrow$ Sublinear TF-IDF $(1,2)$ N-grams $\rightarrow$ Platt-Calibrated Linear SVM.
  - *Engine 2 (Factual LLM):* Google Gemini 2.5 Flash SDK with prompt firewall.
  - *Consensus Arbiter:* Reconciles verdicts into `AGREE`, `DISAGREE`, or `INCONCLUSIVE`.
- **Persistence Tier:** 11 normalized tables via SQLAlchemy ORM (SQLite / MySQL).
> **Speaker Notes:**  
> "Here is our four-tier architecture. Notice how the request first checks our SHA-256 content cache to prevent redundant work. When new text arrives, it flows through our deterministic linguistic SVM for sub-2ms stylometric scoring and can be cross-verified against Gemini's live knowledge base."

---

### Slide 4: Engine 1 — NLP Pipeline & Calibrated Linear SVM
- **NLP Preprocessing:** Lowercasing, regex URL stripping, punctuation removal, stopword filtering.
- **Headline Weighting ($2\times$):** $\text{Processed Text} = \text{Title} + \text{" "} + \text{Title} + \text{" "} + \text{Article}$.
- **Feature Extraction:** Sublinear TF-IDF ($1 + \log(TF)$) with unigrams & bigrams across 5,000 dimensions.
- **Champion Algorithm:** Linear Support Vector Machine (`LinearSVC`).
- **Platt Scaling (`CalibratedClassifierCV`):** Fits a 3-fold cross-validated logistic sigmoid over SVM margins:
  $$P(\text{REAL} \mid x) = \frac{1}{1 + \exp(A \cdot f(x) + B)}$$
  Converts raw distances into true confidence probabilities between 0.0 and 1.0.
> **Speaker Notes:**  
> "We chose Linear SVM because text in 5,000-dimensional space is linearly separable, and SVM constructs the maximum-margin hyperplane. Since raw SVM outputs signed distances rather than probabilities, we implemented 3-fold Platt Scaling to produce true mathematical probabilities."

---

### Slide 5: Phase 2 — Dataset Expansion & Harmonization
- **Total Corpus Size:** Expanded from 72 records to **684 records** (~10x growth).
- **Class Balance:** **343 REAL (50.15%) vs 341 FAKE (49.85%)**.
- **Combinatorial 500-Record Expansion:** Synthesized 250 unique Real and 250 unique Fake records across 8 domains (Tech, Health, Politics, Finance, Space/ISRO, Infrastructure, Education, Sports).
- **Cryptographic Deduplication:** SHA-256 hashing resulted in **zero duplicate collisions (100% unique)**.
- **Integrity Validation:** 0 null values, valid binary labels, passed automated schema audit.
> **Speaker Notes:**  
> "A machine learning model is only as good as its data. In Phase 2, we scaled our training corpus to 684 balanced records across 8 diverse domains, ensuring the model generalizes well beyond narrow political topics."

---

### Slide 6: Phase 3 — Empirical Results & Benchmark Evaluation
- **Overall Test Accuracy:** **98.54%** (Holdout test split of 137 unseen samples).
- **Macro F1 Score:** **0.9854** | **Real Class F1:** **0.9857**.
- **ROC-AUC Score:** **1.0000** (Perfect separability).
- **Real News Recall:** **100.0%** (Zero authentic articles misclassified as fake).
- **Fake News Precision:** **100.0%** (Zero false accusations).
- **Confusion Matrix:**
  $$\begin{bmatrix} 66 & 2 \\ 0 & 69 \end{bmatrix}$$
> **Speaker Notes:**  
> "On our independent 20% holdout test set of 137 samples, the champion Calibrated Linear SVM achieved 98.54% accuracy and 1.000 ROC-AUC. Crucially, recall on authentic news was 100%, meaning our system never falsely flags genuine journalism as fake."

---

### Slide 7: Engine 2 — Google Gemini 2.5 Flash & Consensus Engine
- **SDK:** Official `google-genai` Python SDK.
- **Prompt Injection Firewall:** Treats news text strictly as untrusted data; ignores internal instructions.
- **Enforced JSON Output:** `assessment`, `confidence_score`, `evidence_summary`, `sources`.
- **Consensus States:**
  - `AGREE`: Both engines concur on REAL or FAKE (maximum confidence).
  - `DISAGREE`: Conflicting verdicts $\rightarrow$ `INCONCLUSIVE (CONFLICT)` routed to admin human review.
  - `INCONCLUSIVE`: Confidence below 60% threshold.
> **Speaker Notes:**  
> "Our second engine runs Google Gemini 2.5 Flash. We designed a strict prompt firewall so malicious users cannot inject commands into article bodies. The Consensus Arbiter reconciles both engines: if they disagree, it flags a conflict for human review rather than guessing."

---

### Slide 8: Relational Database & Telemetry (11 Tables)
- **Tables 1–6 (User & Prediction Telemetry):** `users`, `admins`, `news`, `prediction_history`, `saved_news`, `uploaded_files`.
- **Tables 7–11 (Governance & Model Auditing):** `datasets`, `gemini_verification`, `model_versions`, `training_logs`, `admin_logs`.
- **Deduplication:** SHA-256 content hashes prevent duplicate article storage and speed up repeated queries.
- **Dual Support:** SQLite developer database (`fake_news_dev.db`) + enterprise MySQL 8.0 support.
> **Speaker Notes:**  
> "We designed 11 normalized relational database tables. Every prediction, confidence score, user bookmark, and administrator retraining action is tracked with full auditability."

---

### Slide 9: User Workspace & Administrator Governance Portals
- **Citizen User Workspace:**
  - Real-time prediction with animated confidence gauges and salient keyword badges (`#quantum`, `#cryogenic`).
  - Dual-engine live claim analysis interface.
  - Multi-format file ingestion (PDF, Word DOCX, TXT, CSV) with batch inference.
  - Personal saved news bookmarking.
- **Administrator Intelligence Console:**
  - Global KPI counters and Chart.js prediction distribution charts.
  - Dataset schema validation modal.
  - Model retraining console with live confusion matrix and rollback capability.
> **Speaker Notes:**  
> "Our frontend provides two distinct portals: a citizen user interface for quick claim checks, file uploads, and bookmarks, and an administrative console for dataset validation, retraining, and system governance."

---

### Slide 10: Multi-Format Document Ingestion Engine
- **PDF Documents:** Page-by-page text extraction and header/footer stripping via `pypdf`.
- **Word Documents (`.docx`):** Paragraph and heading parser via `python-docx`.
- **Plain Text (`.txt`):** Structured headline and body isolation.
- **Spreadsheets (`.csv`):** Bulk row ingestion and automated column mapping via `pandas`.
> **Speaker Notes:**  
> "Misinformation often spreads via leaked memos or forward PDFs. Our document ingestion engine extracts text directly from PDF, Word, and CSV files, enabling batch inference across dozens of articles simultaneously."

---

### Slide 11: Software Engineering, Security & Pytest Suite
- **Automated Testing:** 15 automated Pytest unit tests passing with **100% success rate**.
- **Cryptographic Security:** Salted PBKDF2 password hashing, JWT role guards (`@admin_required()`).
- **File Upload Security:** File extension filtering (strictly rejecting `.exe`, `.sh`, `.py`).
- **Environment Stability:** Re-compiled and serialized natively on Python 3.13 and Scikit-Learn 1.9.1 with zero version warnings.
> **Speaker Notes:**  
> "To guarantee production quality, we implemented 15 automated Pytest unit tests covering authentication, token expiration, file security, and prediction determinism. All 15 tests pass with a 100% success rate."

---

### Slide 12: Conclusion & Future Scope
- **Key Achievements:**
  - Production-ready full-stack platform with sub-2ms deterministic ML and live LLM verification.
  - 98.54% accuracy and 100% recall on authentic news on our 684-record balanced corpus.
- **Future Directions:**
  - Multilingual NLP support for regional Indian languages (Hindi, Marathi, Tamil, Bengali).
  - Multimodal computer vision models to detect deepfake images and videos.
  - Chrome browser extension for real-time social media feed auditing.
- **Final Slide:** Thank you / Questions & Answers.
> **Speaker Notes:**  
> "In conclusion, our dual-engine architecture demonstrates how classical machine learning and modern generative AI can complement each other to solve complex societal problems. Thank you, and we welcome your questions."
