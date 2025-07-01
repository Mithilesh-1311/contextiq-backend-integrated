"""
AI Utility functions for summarization and flashcard generation.

This module wraps the core natural-language processing needed by the
ContextIQ backend so that the rest of the application can stay
lightweight and focused on routing / persistence.
"""

import io
import collections

import pdfplumber
import PyPDF2
import nltk
from transformers import pipeline

# Download punkt silently on first run
nltk.download("punkt", quiet=True)

# Initialise the summariser once at import time
# BART-Large CNN is a strong, general-purpose abstractive summariser
_summariser = pipeline("summarization", model="facebook/bart-large-cnn")

def _pdf_bytes_to_text(file_storage):
    """Read an uploaded PDF file and return its concatenated text."""
    raw = file_storage.read()
    # First try pdfplumber – better layout preservation
    try:
        text = ""
        with pdfplumber.open(io.BytesIO(raw)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception:
        # Fallback to PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(raw))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return text.strip()

def summarise_file(file_storage, *, max_chunk_chars=3500):
    """Return an abstractive summary of the uploaded PDF."""
    text = _pdf_bytes_to_text(file_storage)
    if not text:
        return "No extractable text found in the PDF."

    # HuggingFace pipelines have a 1024‑token limit; we slice the text
    chunks = [text[i:i + max_chunk_chars] for i in range(0, len(text), max_chunk_chars)]
    partial_summaries = []
    for chunk in chunks:
        res = _summariser(chunk, max_length=180, min_length=30, do_sample=False)[0]["summary_text"]
        partial_summaries.append(res.strip())
    # Summarise the summaries if the result is very long
    combined = " ".join(partial_summaries)
    if len(combined.split()) > 220:
        combined = _summariser(combined, max_length=220, min_length=80, do_sample=False)[0]["summary_text"]
    return combined

def generate_flashcards(file_storage, *, top_n=12):
    """Return a basic set of Q‑A flashcards derived from key noun‑phrases."""
    import spacy
    text = _pdf_bytes_to_text(file_storage)
    if not text:
        return []

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    noun_phrases = [chunk.text.lower() for chunk in doc.noun_chunks if 2 <= len(chunk.text.split()) <= 5]
    keywords = [kw for kw, _ in collections.Counter(noun_phrases).most_common(top_n)]

    cards = []
    for kw in keywords:
        cards.append({
            "question": f"What is {kw}?",
            "answer": f"{kw.capitalize()} is a key concept discussed in the document.",
        })
    return cards

def generate_notes_template(file_storage):
    """Generate a notes template from the uploaded PDF."""
    text = _pdf_bytes_to_text(file_storage)
    if not text:
        return "No extractable text found in the PDF."
    # Simple template: extract headings and key sections
    import re
    headings = re.findall(r'\n([A-Z][A-Za-z0-9\s:,-]{3,})\n', text)
    template = "Notes Template\n\n"
    for idx, heading in enumerate(headings[:8], 1):
        template += f"{idx}. {heading.strip()}\n   - Main Points:\n   - Examples:\n   - Questions:\n\n"
    if not headings:
        template += "(No clear headings found. Use bullet points below.)\n- Point 1:\n- Point 2:\n"
    return template
