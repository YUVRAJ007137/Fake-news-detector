# Automated Testing Report: AI Based Fake News Detection System

## 1. Executive Summary

This report documents the verification and automated testing of the **AI Based Fake News Detection System**. Testing was executed across both backend Python microservices (Pytest) and the React.js client build toolchain (Vite Rollup).

- **Total Test Cases Executed**: 15
- **Passed**: 15
- **Failed**: 0
- **Pass Rate**: 100.0%
- **Frontend Production Build**: Successful (`dist/` generated with 0 errors)

---

## 2. Test Execution Log (Pytest 9.1.1 on Python 3.14.2)

```text
============================= test session starts =============================
platform win32 -- Python 3.14.2, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\Users\rohit\OneDrive\Desktop\current
collected 15 items

backend/tests/test_auth.py::test_user_registration_success PASSED        [  6%]
backend/tests/test_auth.py::test_user_registration_duplicate_email PASSED [ 13%]
backend/tests/test_auth.py::test_user_login_success PASSED               [ 20%]
backend/tests/test_auth.py::test_admin_registration_rejects_without_secret PASSED [ 26%]
backend/tests/test_auth.py::test_admin_registration_success_with_valid_secret PASSED [ 33%]
backend/tests/test_dataset_validation.py::test_validate_self_generated_dataset PASSED [ 40%]
backend/tests/test_dataset_validation.py::test_validate_hybrid_dataset PASSED [ 46%]
backend/tests/test_file_parser.py::test_extract_text_txt PASSED          [ 53%]
backend/tests/test_file_parser.py::test_process_csv_batch PASSED         [ 60%]
backend/tests/test_file_parser.py::test_reject_unsupported_extensions PASSED [ 66%]
backend/tests/test_gemini_service.py::test_gemini_unconfigured_offline_degradation PASSED [ 73%]
backend/tests/test_ml_pipeline.py::test_clean_text_removes_stopwords_and_urls PASSED [ 80%]
backend/tests/test_ml_pipeline.py::test_combine_title_and_article_weighting PASSED [ 86%]
backend/tests/test_ml_pipeline.py::test_prediction_service_inference_bounds PASSED [ 93%]
backend/tests/test_ml_pipeline.py::test_prediction_hash_determinism PASSED [100%]

======================= 15 passed, 7 warnings in 17.48s =======================
```

---

## 3. Test Cases Breakdown & Coverage Matrix

| Test ID | Test Category | Description | Input / Condition | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Auth | User Registration | Valid citizen credentials | 201 Created with role `user` | **PASSED** |
| **TC-02** | Auth | Duplicate Email Prevention | Same email twice | 409 Conflict with clear error | **PASSED** |
| **TC-03** | Auth | User Authentication | Valid password | 200 OK with signed JWT | **PASSED** |
| **TC-04** | Security | Admin Secret Guard | Unregistered secret | 403 Forbidden rejection | **PASSED** |
| **TC-05** | Security | Admin Enrollment | Valid enrollment secret | 201 Created with role `admin` | **PASSED** |
| **TC-06** | Data | Self-Generated Dataset | 48 synthetic & verified rows | Valid schema, 0 nulls, 0 dups | **PASSED** |
| **TC-07** | Data | Hybrid Dataset Integrity | 72 merged rows | Balanced classes (36:36), 0 dups | **PASSED** |
| **TC-08** | Ingestion | Plain Text Document Parsing | TXT file | Extracted title & body lines | **PASSED** |
| **TC-09** | Ingestion | Batch CSV Processing | 2-row test CSV | Row-by-row ML inference | **PASSED** |
| **TC-10** | Security | File Upload Extension Guard | `.exe` and `.py` payload | Rejected by whitelist | **PASSED** |
| **TC-11** | Resilience | Gemini Offline Degradation | Missing API key | Clean fallback to local ML | **PASSED** |
| **TC-12** | NLP | Stopwords & URL Removal | Headline with URLs | URLs and stopwords stripped | **PASSED** |
| **TC-13** | NLP | Weighted Text Collocation | Title and article text | Title duplicated for salience | **PASSED** |
| **TC-14** | ML | Probability Range Validation | Scientific article | Probabilities bounded in $[0, 1]$ | **PASSED** |
| **TC-15** | Performance | Deterministic Hashing | Identical news texts | Same SHA-256 hash | **PASSED** |

---

## 4. Frontend Build Test

- **Tool**: Vite v6.4.5 + Rollup
- **Command**: `npm.cmd --prefix frontend run build`
- **Result**:
  - `dist/index.html`: `0.78 kB`
  - `dist/assets/index-*.css`: `248.78 kB`
  - `dist/assets/index-*.js`: `639.09 kB`
  - **Status**: Completed in `11.79s` with 0 syntax or bundling errors.
