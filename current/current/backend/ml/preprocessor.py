"""
Module: preprocessor.py
Description: Natural Language Processing (NLP) text preprocessing, cleaning,
             tokenization, and stop-word filtering for fake news classification.
"""

import re
import string

# Standard English stopwords list embedded directly to eliminate runtime download failures
ENGLISH_STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
    "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both",
    "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't",
    "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't",
    "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll",
    "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's",
    "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once",
    "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same",
    "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such",
    "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there",
    "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those",
    "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd",
    "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where",
    "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't",
    "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
    "yourself", "yourselves"
}

def clean_text(text: str) -> str:
    """
    Cleans raw news text by stripping URLs, emails, HTML entities, punctuation,
    converting to lowercase, and removing common stopwords.
    """
    if not isinstance(text, str):
        return ""

    # Strip HTML tags
    text = re.sub(r"<[^>]+>", " ", text)
    # Strip URLs
    text = re.sub(r"http[s]?://\S+", " ", text)
    # Strip Emails
    text = re.sub(r"\S+@\S+", " ", text)
    # Lowercase
    text = text.lower()
    # Strip punctuation & digits
    text = re.sub(r"[%s\d]" % re.escape(string.punctuation), " ", text)
    # Tokenize by whitespace
    tokens = text.split()
    # Remove stopwords and short tokens (< 3 chars)
    filtered = [w for w in tokens if w not in ENGLISH_STOPWORDS and len(w) > 2]

    return " ".join(filtered)

def combine_title_and_article(title: str, article: str) -> str:
    """
    Constructs a weighted textual representation combining title and body.
    Titles carry high informational salience in fake news detection.
    """
    clean_t = clean_text(title or "")
    clean_a = clean_text(article or "")
    # Title repeated twice to give it proportional semantic weight in TF-IDF
    return f"{clean_t} {clean_t} {clean_a}".strip()
