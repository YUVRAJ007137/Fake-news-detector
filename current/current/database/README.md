# Database Design & Setup Guide: Fake News Detection System

This directory houses relational database scripts, schemas, and seeds for the **AI Based Fake News Detection System** targeting MySQL 8.0+.

## Database Architecture

The relational schema implements 11 normalized tables ensuring referential integrity, indexing for high-frequency queries, and auditability:

| Table | Purpose | Primary Key | Foreign Keys |
| :--- | :--- | :--- | :--- |
| `users` | User accounts, credentials, and role designation (`user` / `admin`) | `id` | - |
| `admins` | Strict administrator authorization records | `id` | `user_id` -> `users.id` |
| `news` | Ingested news articles, titles, sources, and SHA-256 hashes | `id` | - |
| `prediction_history` | Persistent ML & LLM classification logs and confidence | `id` | `user_id`, `news_id` |
| `saved_news` | User bookmarked news articles | `id` | `user_id`, `news_id` |
| `uploaded_files` | Metadata for batch PDF/DOCX/CSV/TXT uploads | `id` | `user_id` |
| `datasets` | Provenance tracking for self-generated, Kaggle, and hybrid datasets | `id` | - |
| `gemini_verification`| LLM claim verification, citations, and agreement status | `id` | `prediction_history_id` |
| `model_versions` | Champion and challenger ML model registries & metrics | `id` | - |
| `training_logs` | Audit trail of background model retraining runs | `id` | - |
| `admin_logs` | Security log of administrative system actions | `id` | `admin_id` -> `users.id` |

## Setup Instructions (MySQL 8.0+)

### 1. Log in to MySQL as root:
```bash
mysql -u root -p
```

### 2. Execute the schema script:
```sql
SOURCE database/schema.sql;
```

### 3. Execute the seed script:
```sql
SOURCE database/seed.sql;
```

### 4. Create a dedicated application user (Optional but Recommended):
```sql
CREATE USER IF NOT EXISTS 'fakenews_user'@'localhost' IDENTIFIED BY 'FakenewsPass2025!';
GRANT ALL PRIVILEGES ON fake_news_detection.* TO 'fakenews_user'@'localhost';
FLUSH PRIVILEGES;
```

### 5. Automated Python Initialization
Alternatively, use the provided script to automatically initialize the tables and seeds:
```bash
python database/init_db.py
```
*(Supports both MySQL and SQLite local fallback mode)*
