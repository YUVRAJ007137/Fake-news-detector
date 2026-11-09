# Data Flow Diagrams (DFD): Levels 0, 1, and 2

## DFD Level 0 (Context Diagram)

The Level 0 context diagram demonstrates external entities interacting with the centralized system boundary.

```mermaid
graph LR
    User["End User (Citizen / Researcher)"]
    Admin["System Administrator"]
    Gemini["Google Gemini LLM Service"]
    System(("0.0<br/>AI Based Fake News<br/>Detection System"))
    MySQL[("MySQL Relational<br/>Database")]

    User -->|Submit News / Upload Documents| System
    System -->|Prediction Verdict & Confidence| User

    Admin -->|Retrain Trigger & Dataset Upload| System
    System -->|System KPIs & Audit Telemetry| Admin

    System -->|Claim Verification Query| Gemini
    Gemini -->|Factual Evidence & Citations| System

    System <-->|Read / Write History & Models| MySQL
```

---

## DFD Level 1 (Major System Subsystems)

DFD Level 1 decomposes the application into its primary operational components.

```mermaid
graph TD
    User["User"]
    Admin["Administrator"]

    P1(("1.0<br/>Authentication &<br/>Authorization"))
    P2(("2.0<br/>Previous News<br/>ML Inference"))
    P3(("3.0<br/>Latest News<br/>LLM Verification"))
    P4(("4.0<br/>Document Extraction<br/>& Parsing"))
    P5(("5.0<br/>Dataset & Retraining<br/>Pipeline"))

    D1[("Users & Admins Store")]
    D2[("News & Prediction History")]
    D3[("Model Artifacts & Datasets")]

    User -->|Credentials| P1
    Admin -->|Admin Secret & Credentials| P1
    P1 <-->|Verify Hashes| D1

    User -->|Headline & Article| P2
    P2 <-->|Check Hash Cache| D2
    P2 <-->|TF-IDF & Weights| D3
    P2 -->|Save Prediction| D2

    User -->|Current Claims| P3
    P3 -->|External API Call| GeminiAPI["Google GenAI API"]
    GeminiAPI -->|Evidence Summary| P3
    P3 -->|Store Consensus| D2

    User -->|PDF / DOCX / TXT / CSV| P4
    P4 -->|Extracted Text| P2
    P4 -->|Audit Log| D2

    Admin -->|Upload / Validate / Retrain| P5
    P5 <-->|Hybrid Merge & Serialize| D3
```

---

## DFD Level 2 (Dual-Engine Prediction Pipeline)

Detailed data flow of Process 2.0 and Process 3.0 during text analysis.

```mermaid
graph TD
    RawInput["Raw News Title & Article Body"]

    P2_1(("2.1<br/>Text Normalization<br/>& SHA-256 Hashing"))
    P2_2(("2.2<br/>Cache Lookup"))
    P2_3(("2.3<br/>Stopword Stripping<br/>& N-gram TF-IDF"))
    P2_4(("2.4<br/>Calibrated SVM<br/>Inference"))
    P2_5(("2.5<br/>Gemini Claim<br/>Prompt Evaluation"))
    P2_6(("2.6<br/>Consensus Arbiter<br/>& Signal Extraction"))
    P2_7(("2.7<br/>Relational<br/>Persistence"))

    RawInput --> P2_1
    P2_1 -->|Content Hash| P2_2
    P2_2 -->|Cache Hit| ResultOutput["Formatted Prediction Output"]
    P2_2 -->|Cache Miss| P2_3

    P2_3 -->|Sparse Feature Vector| P2_4
    P2_4 -->|Class Probabilities| P2_6

    P2_1 -->|Raw Text (If Latest Mode)| P2_5
    P2_5 -->|LLM Evidence & Verdict| P2_6

    P2_6 -->|Consensus Verdict & Confidence| P2_7
    P2_7 -->|Return JSON| ResultOutput
    P2_7 -->|INSERT SQL| DB[("MySQL Database")]
```
