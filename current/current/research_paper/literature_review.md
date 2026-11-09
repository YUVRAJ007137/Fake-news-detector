# Comprehensive Literature Review: Fake News Detection Paradigms

## 1. The Epistemological Landscape of Digital Deception

Misinformation, disinformation, and malinformation represent distinct vectors within information disorder (Wardle & Derakhshan, 2017).
- **Disinformation**: Information that is deliberately false and maliciously disseminated.
- **Misinformation**: Information that is false, but not created with the intention of causing harm.
- **Malinformation**: Information based on reality, used to inflict harm (e.g., weaponized leaks).

In computational linguistics, fake news detection is predominantly framed as a binary classification problem: distinguishing authentic journalism from fabricated assertions.

---

## 2. Stylometric & Linguistic Approaches

Early computational efforts focused on stylometric markers (Perez-Rosas et al., 2018). Deceptive text exhibits measurable statistical divergence from verified reporting:
1. **Hyperbolic Lexicon**: Overuse of emotional intensifiers and superlative adjectives.
2. **Syntactic Simplicity**: Lower average sentence lengths and reduced subordination.
3. **Punctuation Anomalies**: Excessive capitalization, exclamation marks, and informal typographic emphasis.

Ahmed et al. (2018) demonstrated that Term Frequency-Inverse Document Frequency (TF-IDF) combined with Linear Support Vector Machines achieves robust baseline classification across political corpora by capturing both lexical choice and structural collocations.

---

## 3. Large Language Models (LLMs) & Fact-Checking

Recent breakthroughs in foundation models (Google DeepMind, 2024; Touvron et al., 2023) have enabled generative claim analysis. While LLMs excel at cross-referencing semantic claims with internal parametric weights, they present distinct limitations:
1. **Hallucination Risk**: Large generative models can hallucinate plausible-sounding citations.
2. **Computational Overhead**: Invoking billion-parameter models for trivial stylometric filtering is resource-prohibitive.
3. **Temporal Cutoffs**: Static weights cannot authenticate events occurring after pre-training without retrieval augmentation.

---

## 4. The Proposed Dual-Engine Hybrid Paradigm

This research addresses these limitations by pairing **Calibrated Classical Machine Learning** with **Prompt-Secured LLM Claim Verification**. The classical pipeline handles instantaneous stylometric classification ($<2\text{ ms}$ latency), while the LLM engine performs factual validation for current events, arbitrated through an explicit consensus model.
