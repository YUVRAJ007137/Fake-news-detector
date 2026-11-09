# System Architecture Diagram: AI Based Fake News Detection System

The system implements a decoupled client-server architecture with dual inference engines (Classical ML + LLM Verification) and relational persistence.

```mermaid
graph TD
    subgraph ClientLayer ["Client Layer (React.js Frontend)"]
        UI_User["User Dashboard<br/>(Previous News, Latest News, File Upload)"]
        UI_Admin["Admin Console<br/>(Retraining, Datasets, User Governance)"]
        UI_State["AuthContext & Axios Client<br/>(JWT Interceptor)"]
    end

    subgraph GatewayLayer ["API Gateway & Application Layer (Python Flask)"]
        API_Auth["Auth Blueprint<br/>(/api/auth & /api/admin/auth)"]
        API_News["News Blueprint<br/>(/api/news/predict & latest-analysis)"]
        API_Files["File Processing Blueprint<br/>(/api/files/upload)"]
        API_Admin["Admin Operations Blueprint<br/>(/api/admin/models, datasets)"]
    end

    subgraph DualEngineLayer ["Dual-Engine Verification Core"]
        subgraph Engine1 ["Engine 1: Classical Machine Learning"]
            NLP["NLP Cleaning & Stopwords Filter"]
            TFIDF["TF-IDF Vectorizer<br/>(5,000 Unigrams & Bigrams)"]
            SVM["Calibrated Linear SVM<br/>(Platt Scaling Posterior Probs)"]
        end

        subgraph Engine2 ["Engine 2: LLM Claim Verification"]
            GeminiClient["Google GenAI Python SDK<br/>(Gemini 2.5 Flash)"]
            PromptShield["Prompt Security & Claim Extraction"]
        end

        Consensus["Consensus & Conflict Arbiter<br/>(AGREE / DISAGREE / INCONCLUSIVE)"]
    end

    subgraph DataLayer ["Data & Document Storage (MySQL 8.0+)"]
        DB[(MySQL Database<br/>'fake_news_detection'<br/>11 Relational Tables)]
        ModelStore["trained_models/<br/>(fake_news_model.pkl, tfidf_vectorizer.pkl)"]
        DataStore["dataset/<br/>(self_generated, kaggle, hybrid)"]
    end

    UI_User -->|REST / JSON| GatewayLayer
    UI_Admin -->|REST / JSON| GatewayLayer

    API_News --> Engine1
    API_News --> Engine2
    API_Files --> Engine1
    API_Files --> Engine2

    Engine1 --> Consensus
    Engine2 --> Consensus

    GatewayLayer -->|SQLAlchemy ORM| DB
    Engine1 -->|Load Weights| ModelStore
    API_Admin -->|Retrain / Inspect| DataStore
```
