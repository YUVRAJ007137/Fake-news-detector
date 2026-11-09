# Installation & Local Setup Guide

A complete, step-by-step installation and local execution guide for the **AI Based Fake News Detection System** on Windows and Linux systems without XAMPP.

---

## 1. Prerequisites

Ensure the following software packages are installed:
- **Python**: Python 3.12.x or 3.14.x
- **Node.js**: Node.js v18+ with `npm`
- **MySQL**: MySQL Server 8.0+ (the system also supports an instant local SQLite fallback mode if MySQL credentials are not yet configured)

---

## 2. Windows Step-by-Step Execution Commands

Open Windows PowerShell in the project directory:
`c:\Users\rohit\OneDrive\Desktop\current`

### Step 1: Create and Activate Python Virtual Environment (Optional if using system Python)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 2: Install Python Dependencies
```powershell
pip install -r backend/requirements.txt
```

### Step 3: Install Frontend Dependencies
```powershell
npm.cmd --prefix frontend install
```

---

## 3. Database Setup (MySQL 8.0+)

### Option A: Using Local MySQL Server (`MySQL80`)
1. Log in to MySQL client as `root`:
   ```powershell
   mysql -u root -p
   ```
2. Execute the schema script:
   ```sql
   SOURCE database/schema.sql;
   SOURCE database/seed.sql;
   ```
3. Update `backend/.env` with your password:
   ```env
   DB_USER=root
   DB_PASSWORD=your_actual_mysql_password
   USE_SQLITE_FALLBACK=false
   ```
4. Run the automated Python initialization script:
   ```powershell
   python database/init_db.py
   ```

### Option B: Instant Local SQLite Fallback (Zero Setup)
If you wish to test the system immediately without MySQL configuration:
1. Ensure `USE_SQLITE_FALLBACK=true` in `backend/.env`.
2. Run:
   ```powershell
   python database/init_db.py
   ```
   *(Creates tables and seeds default users inside `backend/fake_news_dev.db` automatically)*

---

## 4. Dataset Preparation & ML Model Training

Execute the reproducible automated data engineering and training pipeline:

```powershell
# 1. Generate the self-generated news corpus (48 records across 6 sectors)
python scripts/generate_self_dataset.py

# 2. Prepare the Kaggle/ISOT benchmark dataset (24 records)
python scripts/prepare_kaggle_dataset.py

# 3. Construct the harmonized hybrid dataset (72 balanced records)
python scripts/create_hybrid_dataset.py

# 4. Validate dataset schema, missing values, and labels
python scripts/validate_datasets.py

# 5. Train and calibrate candidate models (Logistic Regression vs. Linear SVM)
python scripts/train_model.py

# 6. Evaluate model on test split and inspect confusion matrix
python scripts/evaluate_model.py
```

---

## 5. Starting the Applications

### Terminal 1: Start Python Flask Backend (Port 5000)
```powershell
python backend/app.py
```
*Backend will be live at: `http://127.0.0.1:5000`*
*Health check: `http://127.0.0.1:5000/api/health`*

### Terminal 2: Start React Vite Frontend (Port 5173)
```powershell
npm.cmd --prefix frontend run dev
```
*Frontend application will be accessible in your web browser at: `http://localhost:5173`*

---

## 6. Running Automated Tests

Run the full pytest suite:
```powershell
pytest backend/tests -v
```

Run frontend production bundle verification:
```powershell
npm.cmd --prefix frontend run build
```

---

## 7. Default Credentials Reference

| Role | Email | Password | Access Route |
| :--- | :--- | :--- | :--- |
| **System Administrator** | `admin@fakenews.ai` | `Admin@12345` | `/admin/login` |
| **Research Student (User)** | `user@fakenews.ai` | `User@12345` | `/login` |
| **Admin Enrollment Secret** | - | `AdminSecretPasscode2025!` | `/admin/register` |
