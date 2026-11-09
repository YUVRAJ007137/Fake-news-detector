# Administrator Manual: AI Based Fake News Detection System

This guide outlines administrative governance, dataset management, candidate model retraining, and system security operations for administrators of the **VeriNews** platform.

---

## 1. Accessing the Administrator Portal

1. Navigate to `http://localhost:5173/admin/login`.
2. Enter your administrator credentials.
   *(Default Admin: `admin@fakenews.ai` / `Admin@12345`)*
3. **Enrolling a New Administrator**:
   - Navigate to `/admin/register`.
   - Provide Full Name, Email, Password, and the **Server Enrollment Secret**.
   - The default bootstrap secret is `AdminSecretPasscode2025!` (configured in `backend/.env`).
   - Registration will be rejected if the secret does not match.

---

## 2. Administrator Dashboard KPIs

The overview console (`/admin/dashboard`) displays real-time system metrics:
- **Registered Users**: Total non-admin citizen accounts.
- **Total Predictions**: Global prediction volume across all modules.
- **Active Model Accuracy**: Verified test accuracy of the active champion model.
- **Prediction Distribution Chart**: Visual doughnut chart showing proportion of Real, Fake, and Inconclusive verdicts.
- **Global Recent Telemetry**: Live stream of latest classification events.

---

## 3. User Governance

1. Click **User Governance** (`/admin/users`) in the left sidebar.
2. View all registered accounts, roles (`user` or `admin`), and status (`Active` or `Deactivated`).
3. Search by name or email.
4. Click **Deactivate** to revoke access for any user account (administrators cannot deactivate their own account).
5. All status toggles are recorded in the immutable `admin_logs` table.

---

## 4. Dataset Operations & Hybrid Construction

1. Click **Dataset Operations** (`/admin/datasets`).
2. The registry lists:
   - `self_generated_news.csv` (Self-generated dataset across 6 domains).
   - `kaggle_news.csv` (Kaggle/ISOT benchmark dataset).
   - `hybrid_dataset.csv` (Unified harmonized dataset).
3. Click **Validate** next to any dataset to run automated integrity audits:
   - Verifies column presence (`news_id`, `title`, `article`, `category`, `source`, `label`, `label_name`).
   - Checks for missing values, nulls, and duplicate records.
   - Reports class balance.
4. Click **Generate / Update Hybrid Dataset** to trigger the automated merging pipeline:
   - Normalizes text and eliminates duplicates using SHA-256 hashes.
   - Rebalances the corpus and outputs an audit report.

---

## 5. Model Retraining & Champion Promotion

1. Click **Retraining & Models** (`/admin/models`).
2. Review the active champion model:
   - Algorithm: **Calibrated Linear Support Vector Machine**.
   - Test Accuracy: **93.3%** | F1 Score: **0.923** | ROC-AUC: **0.964**.
   - Confusion Matrix breakdown.
3. Click **Train Candidate Model**:
   - The backend runs a controlled retraining task comparing Logistic Regression and Calibrated Linear SVM on the latest hybrid dataset.
   - Computes evaluation metrics on an independent 20% stratified test split.
   - If the candidate achieves equal or higher F1 score than the active model, it is automatically promoted to production.
   - Previous versions remain stored in the database for rollback.
4. Review the **Retraining Audit Log** table for past execution statuses.

---

## 6. Gemini Audit & System Logs

- **Gemini Audit Trail (`/admin/gemini-records`)**:
  - Review all LLM verification records, evidence summaries, retrieved sources, and consensus statuses (`AGREE`, `DISAGREE`, `INCONCLUSIVE`).
- **Security Action Logs (`/admin/logs`)**:
  - Full audit trail of administrative actions, user status changes, admin logins, and model promotions with timestamp and administrator ID.
