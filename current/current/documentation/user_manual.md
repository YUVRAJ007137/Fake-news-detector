# User Manual: AI Based Fake News Detection System

This guide outlines end-user operations for citizens, students, and research analysts utilizing the **VeriNews** platform.

---

## 1. Getting Started

1. Open your web browser and navigate to `http://localhost:5173`.
2. Click **User Login** or **Get Started Free**.
3. If you do not have an account, navigate to `/register` and fill in:
   - Full Name
   - Email Address
   - Password (minimum 6 characters)
   - Confirm Password
4. Upon successful registration, log in with your email and password.
   *(Or use the demo account: `user@fakenews.ai` / `User@12345`)*

---

## 2. User Dashboard Overview

After logging in, your home dashboard displays:
- **Lifetime Telemetry**: Total analyzed articles, verified real, flagged fake, and uploaded files.
- **Quick Action Cards**: Direct links to Previous News ML, Latest News Gemini, and File Upload.
- **Recent Prediction History**: A table of your recent queries with status badges.

---

## 3. Detecting Previous News (Trained ML Engine)

1. Click **Previous News ML** in the left sidebar.
2. Enter the **News Headline / Title** and **News Article Content**.
3. Select an appropriate category (e.g., Politics, Health, Science, Technology).
4. *(Optional)* Click **Load Sample Real** or **Load Sample Fake** to pre-fill test articles.
5. Click **Analyze News Authenticity**.
6. The result card displays:
   - Verdict Badge: `REAL` (Green), `FAKE` (Red), or `INCONCLUSIVE` (Amber).
   - Discriminant Confidence Score (e.g., 96.4%).
   - Model explanation and key salient signal terms.
   - Click **Save News** to bookmark the article for future reference.

---

## 4. Analyzing Latest / Breaking News (Dual-Engine Mode)

1. Click **Latest News & Gemini** in the left sidebar.
2. Paste the breaking headline and news claims.
3. Click **Verify News Authenticity**.
4. The system evaluates the claim through both the **Local ML Model** and **Google Gemini**:
   - Compares the semantic signals of the text against trained patterns.
   - Invokes Gemini to assess factual plausibility and extract reference sources.
   - Shows a **Consensus Badge**: `AGREE` if both models match, or `DISAGREE / CONFLICT` if evidence differs.

---

## 5. File Upload Detection

1. Click **File Upload Detection** in the sidebar.
2. Select a file from your computer:
   - **PDF (.pdf)**: Readable text is extracted automatically.
   - **Word (.docx)**: Paragraphs and table content are parsed.
   - **Plain Text (.txt)**: Decoded safely with multi-encoding fallbacks.
   - **CSV (.csv)**: Ingests datasets up to 50 articles and displays a batch table.
3. Select the analysis mode: **Previous News (Local ML)** or **Latest News (ML + Gemini)**.
4. Click **Upload & Process Document**.
5. For batch CSVs, view summary cards and download the full report in JSON format.

---

## 6. Managing History and Bookmarks

- **Prediction History (`/user/history`)**:
  - Filter predictions by `Verified Real`, `Flagged Fake`, or `Inconclusive`.
  - Search using keywords.
  - Click the **Eye icon** on any record to view its full details and Gemini verification notes.
- **Saved News (`/user/saved-news`)**:
  - Review bookmarked articles and delete entries you no longer need.
