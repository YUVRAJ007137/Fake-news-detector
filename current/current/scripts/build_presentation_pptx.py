"""
Script: build_presentation_pptx.py
Description: Generates an executive, university-grade PowerPoint presentation (.pptx)
             for the AI Based Fake News Detection System, formatted for 16:9 widescreen
             with professional cards, tables, metrics, and architecture overviews.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Color Palette
DARK_NAVY = RGBColor(15, 23, 42)       # #0F172A (Primary Background for Title/Dark)
SLATE_BLUE = RGBColor(30, 41, 59)      # #1E293B
BRAND_BLUE = RGBColor(37, 99, 235)     # #2563EB (Accent Blue)
CYAN_ACCENT = RGBColor(14, 165, 233)   # #0EA5E9
TEXT_WHITE = RGBColor(255, 255, 255)
TEXT_DARK = RGBColor(30, 41, 59)
TEXT_MUTED = RGBColor(100, 116, 139)   # #64748B
BG_LIGHT = RGBColor(248, 250, 252)     # #F8FAFC
CARD_BG = RGBColor(255, 255, 255)
BORDER_COLOR = RGBColor(226, 232, 240) # #E2E8F0
SUCCESS_GREEN = RGBColor(16, 185, 129) # #10B981

def create_deck():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Helper: Add standard header
    def add_header(slide, title_text, category="AI BASED FAKE NEWS DETECTION SYSTEM"):
        # Category Pill
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(10), Inches(0.35))
        tf = cat_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = category.upper()
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = BRAND_BLUE

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11), Inches(0.8))
        tf2 = title_box.text_frame
        tf2.word_wrap = True
        p2 = tf2.paragraphs[0]
        p2.text = title_text
        p2.font.size = Pt(24)
        p2.font.bold = True
        p2.font.color.rgb = DARK_NAVY

    # Helper: Add card shape
    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=BORDER_COLOR):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1.5)
        else:
            shape.line.fill.background()
        return shape

    # ==========================================
    # SLIDE 1: TITLE SLIDE (Dark Navy Theme)
    # ==========================================
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = DARK_NAVY
    bg1.line.fill.background()

    # Pill badge
    badge = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.2), Inches(5.2), Inches(0.45))
    badge.fill.solid()
    badge.fill.fore_color.rgb = SLATE_BLUE
    badge.line.color.rgb = BRAND_BLUE
    b_tf = badge.text_frame
    b_p = b_tf.paragraphs[0]
    b_p.text = "MCA / B.TECH FINAL YEAR PROJECT DEFENSE"
    b_p.font.size = Pt(11)
    b_p.font.bold = True
    b_p.font.color.rgb = CYAN_ACCENT
    b_p.alignment = PP_ALIGN.CENTER

    # Title & Subtitle
    t_box = slide1.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(11.3), Inches(2.2))
    t_tf = t_box.text_frame
    t_tf.word_wrap = True
    p1 = t_tf.paragraphs[0]
    p1.text = "AI-Based Fake News Detection System"
    p1.font.size = Pt(38)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.space_after = Pt(14)

    p2 = t_tf.add_paragraph()
    p2.text = "A Dual-Engine News Verification Platform Coupling Platt-Calibrated Linear SVMs & TF-IDF NLP with Google Gemini 2.5 Flash Claim Analysis & Relational Auditing"
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(203, 213, 225)

    # Info cards at bottom
    info_card1 = add_card(slide1, Inches(1.0), Inches(4.7), Inches(3.5), Inches(1.8), bg_color=SLATE_BLUE, border_color=BRAND_BLUE)
    c1_tf = info_card1.text_frame
    c1_tf.word_wrap = True
    c1_p1 = c1_tf.paragraphs[0]
    c1_p1.text = "CLASSIFICATION ENGINE"
    c1_p1.font.size = Pt(11)
    c1_p1.font.bold = True
    c1_p1.font.color.rgb = CYAN_ACCENT
    c1_p2 = c1_tf.add_paragraph()
    c1_p2.text = "• Sublinear TF-IDF (1, 2) N-Grams\n• Calibrated Linear SVM\n• Sub-2ms Deterministic Inference\n• 98.54% Verified Accuracy"
    c1_p2.font.size = Pt(12)
    c1_p2.font.color.rgb = TEXT_WHITE

    info_card2 = add_card(slide1, Inches(4.9), Inches(4.7), Inches(3.5), Inches(1.8), bg_color=SLATE_BLUE, border_color=BRAND_BLUE)
    c2_tf = info_card2.text_frame
    c2_tf.word_wrap = True
    c2_p1 = c2_tf.paragraphs[0]
    c2_p1.text = "FACT-CHECKING ENGINE"
    c2_p1.font.size = Pt(11)
    c2_p1.font.bold = True
    c2_p1.font.color.rgb = CYAN_ACCENT
    c2_p2 = c2_tf.add_paragraph()
    c2_p2.text = "• Google Gemini 2.5 Flash SDK\n• Anti-Prompt Injection Defense\n• Real-Time Factual Verification\n• Automated Consensus Arbiter"
    c2_p2.font.size = Pt(12)
    c2_p2.font.color.rgb = TEXT_WHITE

    info_card3 = add_card(slide1, Inches(8.8), Inches(4.7), Inches(3.5), Inches(1.8), bg_color=SLATE_BLUE, border_color=BRAND_BLUE)
    c3_tf = info_card3.text_frame
    c3_tf.word_wrap = True
    c3_p1 = c3_tf.paragraphs[0]
    c3_p1.text = "ENTERPRISE TELEMETRY"
    c3_p1.font.size = Pt(11)
    c3_p1.font.bold = True
    c3_p1.font.color.rgb = CYAN_ACCENT
    c3_p2 = c3_tf.add_paragraph()
    c3_p2.text = "• 11 Normalized Relational Tables\n• PDF / DOCX / CSV Batch Parsers\n• Full React 18 & Flask 3.1 Stack\n• 15 Automated Pytest Test Suites"
    c3_p2.font.size = Pt(12)
    c3_p2.font.color.rgb = TEXT_WHITE

    # ==========================================
    # SLIDE 2: PROBLEM STATEMENT & MOTIVATION
    # ==========================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "The Problem: Why Traditional Fake News Detectors Fail")

    # Card 1: Linguistic Disinformation
    c1 = add_card(slide2, Inches(0.8), Inches(1.6), Inches(3.6), Inches(5.1))
    tf = c1.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "1. The Linguistic Blindspot"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY
    p = tf.add_paragraph()
    p.text = "\n• Sophisticated disinformation is deliberately drafted using formal, objective, journalistic tone.\n\n• Classical ML alone (Naive Bayes, Random Forests) analyzes style and vocabulary distributions, not real-world factual validity.\n\n• Result: Well-written falsehoods slip right through linguistic filters."
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    # Card 2: The LLM Dilemma
    c2 = add_card(slide2, Inches(4.8), Inches(1.6), Inches(3.6), Inches(5.1))
    tf = c2.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "2. The LLM Cost & Latency Flaw"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY
    p = tf.add_paragraph()
    p.text = "\n• Large Language Models (LLMs) can verify facts, but they are expensive, non-deterministic, and slow (1.5 - 4s per call).\n\n• Vulnerable to Prompt Injection: Malicious articles containing hidden instructions can manipulate LLM verdicts.\n\n• Hallucination risk: LLMs sometimes invent sources or plausible-sounding falsehoods."
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    # Card 3: The Real-World Need
    c3 = add_card(slide2, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.1), bg_color=SLATE_BLUE, border_color=BRAND_BLUE)
    tf = c3.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "3. Our Proposed Solution"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p = tf.add_paragraph()
    p.text = "\n• Dual-Engine Synergy:\nCombine low-latency classical ML (<2ms) for stylistic classification with Google Gemini 2.5 Flash for live factual verification.\n\n• Consensus Arbitration:\nCross-check both engines. If they disagree, flag for human auditing rather than risking false certainty.\n\n• Enterprise Telemetry:\nComplete relational tracking across 11 tables with multi-format document extraction."
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_WHITE

    # ==========================================
    # SLIDE 3: SYSTEM ARCHITECTURE
    # ==========================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "System Architecture: End-to-End Dual-Engine Pipeline")

    arch_card = add_card(slide3, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.1))
    tf = arch_card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Modular Full-Stack Architecture & Information Flow"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = BRAND_BLUE

    p = tf.add_paragraph()
    p.text = """
1. CLIENT TIER (React 18.3 + Vite 6 + Bootstrap 5.3 + Chart.js):
   • Citizen User Portal: Single claim prediction, Gemini claim verification, document batch upload, bookmarks.
   • Admin Intelligence Console: KPI analytics, dataset validation modal, model retraining and confusion matrix review.

2. APPLICATION REST API TIER (Python Flask 3.1):
   • 8 Modular Blueprints: Auth, AdminAuth, News, Files, Datasets, Models, Admin, Health.
   • JWT Token RBAC: Strict cryptographic isolation between citizen users and system administrators.
   • SHA-256 Deduplication Cache: Eliminates redundant inference by instantly retrieving previously audited articles.

3. DUAL-ENGINE INTELLIGENCE TIER:
   • Engine 1 (Classical NLP/ML): Text Preprocessor -> Sublinear TF-IDF (1,2) N-Grams (5,000 features) -> Platt-Calibrated Linear SVM.
   • Engine 2 (Generative LLM): Google Gemini 2.5 Flash via official google-genai SDK with strict prompt firewall.
   • Consensus Arbiter: Reconciles dual-engine verdicts into AGREE, DISAGREE, or INCONCLUSIVE status.

4. PERSISTENCE & TELEMETRY TIER (SQLAlchemy 2.0):
   • 11 Normalized Tables: Users, Admins, News, PredictionHistory, SavedNews, UploadedFiles, Datasets, GeminiVerification, ModelVersions, TrainingLogs, AdminLogs.
   • Dual Configuration: Zero-config SQLite development database & Enterprise MySQL 8.0 support.
"""
    p.font.size = Pt(12)
    p.font.color.rgb = DARK_NAVY

    # ==========================================
    # SLIDE 4: MACHINE LEARNING & NLP PIPELINE
    # ==========================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "Engine 1: Linguistic Feature Extraction & Platt-Calibrated SVM")

    # Step 1: Preprocessing
    s1 = add_card(slide4, Inches(0.8), Inches(1.6), Inches(3.6), Inches(5.1))
    tf = s1.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Step 1: Text Preprocessing"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY
    p = tf.add_paragraph()
    p.text = "\n• Lowercasing & regex URL stripping.\n\n• Symbol and punctuation elimination.\n\n• NLTK English stopword filtering.\n\n• Headline Weighting (2x):\nTitle is concatenated twice with article body:\nTitle + ' ' + Title + ' ' + Article.\nEnsures critical headline clickbait tokens receive double term frequency."
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    # Step 2: TF-IDF
    s2 = add_card(slide4, Inches(4.8), Inches(1.6), Inches(3.6), Inches(5.1))
    tf = s2.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Step 2: Sublinear TF-IDF"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY
    p = tf.add_paragraph()
    p.text = "\n• Feature Space: 5,000 Dimensions.\n\n• N-Gram Range (1, 2):\nCaptures both unigrams ('vaccine', 'moon') and bigram context ('miracle cure', 'green moon', '5g towers').\n\n• Sublinear Term Scaling:\nReplaces raw TF with 1 + log(TF), dampening the influence of repetitive buzzwords."
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    # Step 3: Platt-Calibrated SVM
    s3 = add_card(slide4, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.1), bg_color=SLATE_BLUE, border_color=BRAND_BLUE)
    tf = s3.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Step 3: Calibrated SVM"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p = tf.add_paragraph()
    p.text = "\n• Maximum-Margin Separation:\nLinearSVC constructs an optimal hyperplane across 5,000 dimensions.\n\n• Platt Sigmoidal Scaling:\nRaw SVM outputs uncalibrated signed distances. CalibratedClassifierCV fits a 3-fold cross-validated logistic sigmoid:\nP(REAL | x) = 1 / (1 + exp(A*f(x) + B))\n\n• Converts raw margins to true confidence probabilities between 0.0 and 1.0."
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_WHITE

    # ==========================================
    # SLIDE 5: DATASET EXPANSION & HARMONIZATION
    # ==========================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "Phase 2: Dataset Engineering & 500-Record Expansion")

    # Metrics top row
    m1 = add_card(slide5, Inches(0.8), Inches(1.6), Inches(2.7), Inches(1.5))
    tf = m1.text_frame
    p = tf.paragraphs[0]
    p.text = "TOTAL HYBRID DATASET"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = TEXT_MUTED
    p = tf.add_paragraph()
    p.text = "684"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = BRAND_BLUE
    p = tf.add_paragraph()
    p.text = "Grown from 72 records (~10x)"
    p.font.size = Pt(10)
    p.font.color.rgb = SUCCESS_GREEN

    m2 = add_card(slide5, Inches(3.8), Inches(1.6), Inches(2.7), Inches(1.5))
    tf = m2.text_frame
    p = tf.paragraphs[0]
    p.text = "AUTHENTIC REAL NEWS"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = TEXT_MUTED
    p = tf.add_paragraph()
    p.text = "343"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY
    p = tf.add_paragraph()
    p.text = "50.15% Class Share"
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MUTED

    m3 = add_card(slide5, Inches(6.8), Inches(1.6), Inches(2.7), Inches(1.5))
    tf = m3.text_frame
    p = tf.paragraphs[0]
    p.text = "DECEPTIVE FAKE NEWS"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = TEXT_MUTED
    p = tf.add_paragraph()
    p.text = "341"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY
    p = tf.add_paragraph()
    p.text = "49.85% Class Share"
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MUTED

    m4 = add_card(slide5, Inches(9.8), Inches(1.6), Inches(2.7), Inches(1.5))
    tf = m4.text_frame
    p = tf.paragraphs[0]
    p.text = "DEDUPLICATION RATE"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = TEXT_MUTED
    p = tf.add_paragraph()
    p.text = "100%"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = SUCCESS_GREEN
    p = tf.add_paragraph()
    p.text = "0 Duplicate Collisions"
    p.font.size = Pt(10)
    p.font.color.rgb = SUCCESS_GREEN

    # Bottom summary card
    d_card = add_card(slide5, Inches(0.8), Inches(3.3), Inches(11.7), Inches(3.4))
    tf = d_card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Domain Coverage & Quality Engineering"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY
    p = tf.add_paragraph()
    p.text = """
• 500-Record Combinatorial Synthesis: Programmatically generated 250 unique Real and 250 unique Fake articles using scripts/generate_500_records.py with dynamic named entities, institutions, and metrics.
• Broad Domain Diversity: Encompasses Technology (AI, semiconductors), Healthcare (clinical trials, miracle cures), Politics (cabinet policies, forged circulars), Finance (RBI rules, ATM bans), Science (ISRO propulsion, green moon hoaxes), Infrastructure, Education, and Sports.
• Cryptographic Deduplication: SHA-256 hash checks applied across all titles and bodies, guaranteeing zero sample overlap.
• Automated Validation (scripts/validate_datasets.py): Passed 100% with 0 missing values, valid binary labels, and perfect balance.
• SQLite Database Synchronization: Updated datasets registry table to reflect version v2.0.0.
"""
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 6: EMPIRICAL RESULTS & BENCHMARKS
    # ==========================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "Phase 3: Empirical Model Performance & Evaluation")

    # Table of Results
    rows = 7
    cols = 4
    left = Inches(0.8)
    top = Inches(1.6)
    width = Inches(7.5)
    height = Inches(4.8)

    table_shape = slide6.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    table.columns[0].width = Inches(2.7)
    table.columns[1].width = Inches(1.5)
    table.columns[2].width = Inches(1.5)
    table.columns[3].width = Inches(1.8)

    headers = ["Evaluation Metric", "Version 1.0 (72)", "Logistic Reg (684)", "Calibrated SVM (684)"]
    for col_idx, text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.text = text
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_NAVY
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = TEXT_WHITE

    data = [
        ("Accuracy", "93.33%", "98.54%", "98.54% (Champion)"),
        ("Macro F1 Score", "0.9321", "0.9854", "0.9854"),
        ("Real Class F1", "0.9231", "0.9857", "0.9857"),
        ("ROC-AUC Score", "0.9643", "1.0000", "1.0000 (Perfect)"),
        ("Real News Recall", "85.71%", "100.0%", "100.0% (Zero FN)"),
        ("Fake News Precision", "88.89%", "100.0%", "100.0% (Zero FP)")
    ]

    for row_idx, row_data in enumerate(data):
        for col_idx, val in enumerate(row_data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.text = val
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(11)
                if col_idx == 3:
                    p.font.bold = True
                    p.font.color.rgb = BRAND_BLUE
                else:
                    p.font.color.rgb = DARK_NAVY

    # Confusion Matrix Card on the right
    cm_card = add_card(slide6, Inches(8.7), Inches(1.6), Inches(3.8), Inches(4.8), bg_color=SLATE_BLUE, border_color=BRAND_BLUE)
    tf = cm_card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Holdout Confusion Matrix (137 Samples)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    p = tf.add_paragraph()
    p.text = "\nStratified 80/20 Holdout Partition:\n\n[[ 66,   2 ]   <-- Actual FAKE\n [  0,  69 ]]  <-- Actual REAL\n\n• True Negatives (TN = 66):\n  66 out of 68 fake news items accurately flagged.\n\n• False Positives (FP = 2):\n  Only 2 fake news items escaped threshold.\n\n• False Negatives (FN = 0):\n  Zero authentic articles misclassified as fake!\n\n• True Positives (TP = 69):\n  All 69 authentic news items verified correctly."
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_WHITE

    # ==========================================
    # SLIDE 7: GEMINI LLM & CONSENSUS ARBITRATION
    # ==========================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "Engine 2: Google Gemini GenAI & Consensus Engine")

    g1 = add_card(slide7, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.1))
    tf = g1.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Google Gemini 2.5 Flash SDK Integration"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY
    p = tf.add_paragraph()
    p.text = """
• Official Google GenAI SDK: Integrates directly with Gemini 2.5 Flash for contextual and semantic world-knowledge claim analysis.

• Prompt Injection Defense:
  All user-submitted text is wrapped with strict untrusted data boundaries:
  - Forbids model from obeying commands embedded inside news articles.
  - Neutralizes jailbreak attempts demanding a specific verdict.

• Enforced JSON Schema:
  Outputs structured fields:
  - assessment: 'REAL' | 'FAKE' | 'INCONCLUSIVE'
  - confidence_score: Float (0.0 - 1.0)
  - evidence_summary: Factual justification
  - sources: Authoritative reference outlets

• Offline Degradation: Gracefully degrades to local ML classification if API key is not configured.
"""
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    g2 = add_card(slide7, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1), bg_color=SLATE_BLUE, border_color=BRAND_BLUE)
    tf = g2.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Consensus Arbitration Logic"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p = tf.add_paragraph()
    p.text = """
Cross-Engine Reconciliation Matrix:

1. AGREE Status:
   • Both Classical SVM and Gemini classify as REAL -> Final Decision: REAL
   • Both Classical SVM and Gemini classify as FAKE -> Final Decision: FAKE
   => Maximum reliability and verified authenticity.

2. DISAGREE Status:
   • SVM says REAL, Gemini says FAKE (or vice versa).
   • Final Decision: 'INCONCLUSIVE (CONFLICT)'
   => Automatically flags the record for human administrator review instead of guessing.

3. INCONCLUSIVE Status:
   • Confidence score falls below 60% threshold.
   • Requires secondary verification sources.
"""
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_WHITE

    # ==========================================
    # SLIDE 8: DATABASE & TELEMETRY
    # ==========================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "Database Architecture: 11 Normalized Tables")

    db_card1 = add_card(slide8, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.1))
    tf = db_card1.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "User & Prediction Telemetry Tables"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY
    p = tf.add_paragraph()
    p.text = """
1. users: Citizen and administrator identity records, hashed passwords, active status flags, created_at.
2. admins: Role reference mapping elevating authorized users to administrative privileges.
3. news: Central repository of submitted news articles, deduplicated via SHA-256 content_hash.
4. prediction_history: Comprehensive log of every classification run, confidence score, model version, and mode.
5. saved_news: User bookmarking relationship table linking citizens to validated articles.
6. uploaded_files: Audit record of multi-format document uploads (PDF, DOCX, CSV) and parse statuses.
"""
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    db_card2 = add_card(slide8, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1))
    tf = db_card2.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Governance, Models & Audit Tables"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY
    p = tf.add_paragraph()
    p.text = """
7. datasets: Training dataset registry tracking versions, active flags, and record counts.
8. gemini_verification: Stores live LLM claim assessments, evidence summaries, sources, and agreement statuses.
9. model_versions: Production registry of trained ML model paths, accuracy/F1 evaluation JSON metrics, and is_active flag.
10. training_logs: Audit log of candidate model retraining runs with start/completion times and error states.
11. admin_logs: Immutable security trail capturing all administrative operations with admin_id and timestamps.

Dual-Engine DB Support:
• SQLite dev fallback (fake_news_dev.db) for zero-config operation.
• MySQL 8.0 production compatibility with full relational integrity.
"""
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 9: USER & ADMIN UI PORTALS
    # ==========================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "Frontend Application: Dual-Portal Experience (React 18)")

    u1 = add_card(slide9, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.1))
    tf = u1.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Citizen User Workspace"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = BRAND_BLUE
    p = tf.add_paragraph()
    p.text = """
• User Dashboard: Real-time counters showing total news analyzed, verified authentic, and flagged fake. Recent history audit.
• Previous News ML: Instant sub-2ms classification. Includes sample loader buttons, character counters, confidence meters, and salient term badges.
• Latest News & Gemini: Dual-engine live claim analysis showing consensus breakdown between SVM and Gemini.
• File Ingestion: Drag-and-drop document upload (PDF, Word, TXT, CSV) with batch classification table.
• Saved News: Bookmarked articles stored in personal research collections.
"""
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    u2 = add_card(slide9, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1))
    tf = u2.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Administrator Intelligence Console"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY
    p = tf.add_paragraph()
    p.text = """
• Executive Analytics: System status indicator, global user counters, total prediction telemetry, and Chart.js distribution charts.
• Dataset Operations: One-click schema validation audit modal inspecting row counts, null values, and class balance.
• Model Governance: Live confusion matrix review, accuracy/F1/ROC-AUC metric inspection, and candidate retraining trigger with rollback safety.
• User Governance: User management table with account deactivation toggles.
• Security Action Logs: Timestamped audit trails tracking admin events.
"""
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 10: QUALITY ASSURANCE & PYTEST
    # ==========================================
    slide10 = prs.slides.add_slide(blank_layout)
    add_header(slide10, "Software Engineering: Automated Testing & Verification")

    q_card = add_card(slide10, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.1))
    tf = q_card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Pytest Automated Test Suite: 15 Passed / 0 Failed (100% Pass Rate)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = SUCCESS_GREEN

    p = tf.add_paragraph()
    p.text = """
1. Authentication & Security Tests (backend/tests/test_auth.py):
   • test_user_registration_success: Validates registration, password hashing with PBKDF2/SHA-256.
   • test_user_registration_duplicate_email: Enforces unique email constraint.
   • test_user_login_success: Verifies credential checking and signed JWT access token creation.
   • test_admin_registration_rejects_without_secret: Protects administrative enrollment endpoint.
   • test_admin_registration_success_with_valid_secret: Grants administrative privileges with master passcode.

2. Dataset Schema & Balance Validation (backend/tests/test_dataset_validation.py):
   • test_validate_self_generated_dataset: Confirms 0 nulls, correct binary labels on 660 records.
   • test_validate_hybrid_dataset: Validates 684-record balanced hybrid dataset integrity.

3. Multi-Format File Parser Tests (backend/tests/test_file_parser.py):
   • test_extract_text_txt: Validates plain text headline and body separation.
   • test_process_csv_batch: Tests dynamic CSV column mapping and batch ingestion.
   • test_reject_unsupported_extensions: Security filter rejecting unauthorized executables (.exe, .sh).

4. Gemini Offline Degradation Tests (backend/tests/test_gemini_service.py):
   • test_gemini_unconfigured_offline_degradation: Confirms graceful fallback when API key is unconfigured.

5. Machine Learning Pipeline Tests (backend/tests/test_ml_pipeline.py):
   • test_clean_text_removes_stopwords_and_urls: Validates NLP preprocessor.
   • test_combine_title_and_article_weighting: Verifies 2x headline weighting.
   • test_prediction_service_inference_bounds: Asserts confidence scores are strictly between 0.0 and 1.0.
   • test_prediction_hash_determinism: Asserts SHA-256 deterministic caching behavior.
"""
    p.font.size = Pt(11)
    p.font.color.rgb = DARK_NAVY

    # ==========================================
    # SLIDE 11: CONCLUSION & FUTURE SCOPE
    # ==========================================
    slide11 = prs.slides.add_slide(blank_layout)
    add_header(slide11, "Conclusion & Future Research Directions")

    c1 = add_card(slide11, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.1))
    tf = c1.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Key Project Achievements"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = BRAND_BLUE
    p = tf.add_paragraph()
    p.text = """
• Successfully built a full-stack dual-engine platform combining classical NLP (Platt-Calibrated Linear SVM) with generative factual intelligence (Google Gemini 2.5 Flash).

• Expanded dataset from 72 to 684 balanced records across 8 domains with 0 duplicates.

• Achieved 98.54% test accuracy, 0.9854 Macro F1, 1.0000 ROC-AUC, and 100% recall on authentic news.

• Production-grade engineering with 11 normalized database tables, multi-format file ingestion (PDF, Word, CSV), and 15 automated Pytest tests.

• Zero library version warnings: Retrained and serialized natively on Python 3.13 and Scikit-Learn 1.9.1.
"""
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    c2 = add_card(slide11, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1), bg_color=SLATE_BLUE, border_color=BRAND_BLUE)
    tf = c2.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Future Scope & Enhancements"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p = tf.add_paragraph()
    p.text = """
• Multilingual NLP Support:
  Extend preprocessing and TF-IDF pipelines to regional Indian languages (Hindi, Marathi, Tamil, Bengali).

• Multimodal Deepfake Verification:
  Incorporate computer vision models to detect manipulated images and deepfake videos accompanying articles.

• Browser Extension & Social Media Bot:
  Deploy a lightweight Chrome extension that flags misleading social media posts in real time as users browse digital feeds.

• Continuous Retraining Pipeline:
  Integrate scheduled background pipelines that fetch newly debunked claims from fact-checking APIs to automatically update the training corpus.
"""
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_WHITE

    # ==========================================
    # SLIDE 12: THANK YOU & Q&A
    # ==========================================
    slide12 = prs.slides.add_slide(blank_layout)
    bg12 = slide12.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg12.fill.solid()
    bg12.fill.fore_color.rgb = DARK_NAVY
    bg12.line.fill.background()

    t_box12 = slide12.shapes.add_textbox(Inches(1.5), Inches(2.2), Inches(10.3), Inches(3.0))
    tf12 = t_box12.text_frame
    tf12.word_wrap = True
    p = tf12.paragraphs[0]
    p.text = "Thank You!"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.alignment = PP_ALIGN.CENTER
    p.space_after = Pt(16)

    p2 = tf12.add_paragraph()
    p2.text = "AI-Based Fake News Detection System\nQuestions & Answers"
    p2.font.size = Pt(22)
    p2.font.color.rgb = CYAN_ACCENT
    p2.alignment = PP_ALIGN.CENTER

    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "Fake_News_Detection_Presentation.pptx"))
    prs.save(output_path)
    print(f"[SUCCESS] Presentation saved to: {output_path}")

    # Also save inside project documentation folder
    doc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "documentation", "Fake_News_Detection_Presentation.pptx"))
    prs.save(doc_path)
    print(f"[SUCCESS] Duplicate saved to project docs: {doc_path}")

if __name__ == "__main__":
    create_deck()
