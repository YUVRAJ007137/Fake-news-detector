"""
Service: file_service.py
Description: Secure document parsing service supporting PDF, DOCX, TXT, and CSV
             file uploads for batch fake news classification.
"""

import os
import uuid
import pandas as pd
from werkzeug.utils import secure_filename
from backend.config import Config
from backend.services.prediction_service import PredictionService
from backend.services.gemini_service import GeminiService

class FileService:
    @classmethod
    def allowed_file(cls, filename: str) -> bool:
        return "." in filename and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS

    @classmethod
    def get_extension(cls, filename: str) -> str:
        return filename.rsplit(".", 1)[1].lower() if "." in filename else ""

    @classmethod
    def save_upload(cls, file_storage) -> tuple[str, str, str]:
        """Saves uploaded file securely and returns (original_name, stored_filename, full_path)."""
        original_name = file_storage.filename or "unknown_upload"
        ext = cls.get_extension(original_name)
        if not cls.allowed_file(original_name):
            raise ValueError(f"File extension '.{ext}' is not supported. Allowed formats: PDF, DOCX, TXT, CSV.")

        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        safe_base = secure_filename(original_name.rsplit(".", 1)[0])
        stored_filename = f"{uuid.uuid4().hex[:12]}_{safe_base}.{ext}"
        target_path = os.path.join(Config.UPLOAD_FOLDER, stored_filename)

        file_storage.save(target_path)
        return original_name, stored_filename, target_path

    @classmethod
    def extract_text_pdf(cls, file_path: str) -> tuple[str, str]:
        """Extracts text from a PDF file using pypdf."""
        import pypdf
        reader = pypdf.PdfReader(file_path)
        pages_text = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                pages_text.append(text)

        full_text = "\n\n".join(pages_text).strip()
        if not full_text:
            return "", "The uploaded PDF appears to be empty or contains scanned images without selectable text. An OCR engine is required for scanned documents."

        # Derive title from first line or filename
        lines = [line.strip() for line in full_text.split("\n") if line.strip()]
        title = lines[0][:200] if lines else "Extracted PDF Document"
        article = "\n".join(lines[1:]) if len(lines) > 1 else full_text
        return title, article

    @classmethod
    def extract_text_docx(cls, file_path: str) -> tuple[str, str]:
        """Extracts text from a Word document using python-docx."""
        import docx
        doc = docx.Document(file_path)
        paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

        # Also extract table text if present
        for table in doc.tables:
            for row in table.rows:
                row_text = " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
                if row_text:
                    paragraphs.append(row_text)

        if not paragraphs:
            return "", "The uploaded DOCX file does not contain readable textual paragraphs."

        title = paragraphs[0][:200]
        article = "\n\n".join(paragraphs[1:]) if len(paragraphs) > 1 else paragraphs[0]
        return title, article

    @classmethod
    def extract_text_txt(cls, file_path: str) -> tuple[str, str]:
        """Extracts plain text with encoding fallbacks."""
        for enc in ("utf-8", "latin-1", "cp1252"):
            try:
                with open(file_path, "r", encoding=enc) as f:
                    content = f.read().strip()
                break
            except UnicodeDecodeError:
                continue
        else:
            return "", "Unable to decode the plain text file using standard character encodings."

        lines = [l.strip() for l in content.split("\n") if l.strip()]
        if not lines:
            return "", "The uploaded TXT file is completely empty."

        title = lines[0][:200]
        article = "\n".join(lines[1:]) if len(lines) > 1 else content
        return title, article

    @classmethod
    def process_csv(cls, file_path: str, analysis_mode: str = "ml_previous") -> list[dict]:
        """Parses CSV rows, identifies title/article columns, and runs analysis on each row."""
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            raise ValueError(f"Failed to parse CSV file: {str(e)}")

        # Auto-detect title and article columns
        cols = [c.lower() for c in df.columns]
        title_col = None
        article_col = None

        for c in df.columns:
            cl = c.lower()
            if cl in ("title", "headline", "news_title", "subject") and not title_col:
                title_col = c
            if cl in ("article", "text", "body", "news_article", "content") and not article_col:
                article_col = c

        if not article_col:
            # Fallback: pick the column with the highest average string length
            str_cols = [c for c in df.columns if df[c].dtype == object]
            if str_cols:
                article_col = max(str_cols, key=lambda c: df[c].astype(str).str.len().mean())
            else:
                article_col = df.columns[0]

        if not title_col:
            # Pick the second text column or generate fallback title
            remaining = [c for c in df.columns if c != article_col]
            title_col = remaining[0] if remaining else None

        results = []
        # Limit to first 50 rows to avoid frontend freezing
        sampled_df = df.head(50)

        for idx, row in sampled_df.iterrows():
            title_val = str(row[title_col]) if title_col and pd.notna(row[title_col]) else f"Row {idx+1} News"
            article_val = str(row[article_col]) if pd.notna(row[article_col]) else ""

            if len(article_val.strip()) < 10:
                continue

            ml_result = PredictionService.predict(title_val, article_val, check_cache=True)
            res_item = {
                "row_index": idx + 1,
                "title": title_val[:120],
                "article_preview": article_val[:200] + "...",
                "prediction_label": ml_result.get("prediction_label", "INCONCLUSIVE"),
                "confidence_score": ml_result.get("confidence_score", 0.50),
                "model_version": ml_result.get("model_version", "v1.0.0"),
                "signals": ml_result.get("signals", [])
            }

            if analysis_mode == "gemini_latest":
                gemini_res = GeminiService.analyze_claim(title_val, article_val, ml_label=ml_result.get("prediction_label"))
                res_item["gemini"] = gemini_res
                res_item["overall_decision"] = gemini_res.get("final_decision", ml_result.get("prediction_label"))
            else:
                res_item["overall_decision"] = ml_result.get("prediction_label")

            results.append(res_item)

        return results

    @classmethod
    def process_document(cls, file_path: str, file_type: str, analysis_mode: str = "ml_previous"):
        """Extracts document content and executes the selected detection pipeline."""
        if file_type == "csv":
            row_results = cls.process_csv(file_path, analysis_mode=analysis_mode)
            total = len(row_results)
            real_count = sum(1 for r in row_results if r["overall_decision"] == "REAL")
            fake_count = sum(1 for r in row_results if r["overall_decision"] == "FAKE")
            inconclusive_count = total - (real_count + fake_count)

            return {
                "file_type": "csv",
                "is_batch": True,
                "records_count": total,
                "summary": {
                    "total": total,
                    "real": real_count,
                    "fake": fake_count,
                    "inconclusive": inconclusive_count
                },
                "records": row_results
            }

        # Single document extraction (PDF, DOCX, TXT)
        if file_type == "pdf":
            title, article = cls.extract_text_pdf(file_path)
        elif file_type == "docx":
            title, article = cls.extract_text_docx(file_path)
        elif file_type == "txt":
            title, article = cls.extract_text_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_type}")

        if not article or len(article.strip()) < 15:
            return {
                "file_type": file_type,
                "is_batch": False,
                "records_count": 0,
                "error": article or "No readable text could be extracted from the file."
            }

        ml_result = PredictionService.predict(title, article, check_cache=True)
        output = {
            "file_type": file_type,
            "is_batch": False,
            "records_count": 1,
            "title": title,
            "article": article,
            "prediction_label": ml_result.get("prediction_label", "INCONCLUSIVE"),
            "confidence_score": ml_result.get("confidence_score", 0.50),
            "model_version": ml_result.get("model_version", "v1.0.0"),
            "signals": ml_result.get("signals", []),
            "explanation": ml_result.get("explanation", ""),
            "analysis_mode": analysis_mode
        }

        if analysis_mode == "gemini_latest":
            gemini_res = GeminiService.analyze_claim(title, article, ml_label=ml_result.get("prediction_label"))
            output["gemini"] = gemini_res
            output["overall_decision"] = gemini_res.get("final_decision", ml_result.get("prediction_label"))
        else:
            output["overall_decision"] = ml_result.get("prediction_label")

        return output
