import os
from typing import List, Tuple
from datetime import datetime

import numpy as np
import PyPDF2
import docx
from sqlalchemy.orm import Session

from .hfclient import hf_embed, hf_generate
from .models import File, Chunk

# Upload directory (create if missing)
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./backend/uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


# Text extraction

def extract_text_from_file(path: str, filename: str) -> str:
    """Extract text from txt, pdf, docx files (best-effort)."""
    ext = filename.lower().rsplit(".", 1)[-1]
    if ext == "txt":
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    if ext == "pdf":
        texts = []
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                texts.append(page.extract_text() or "")
        return "\n".join(texts)
    if ext in ("docx", "doc"):
        doc = docx.Document(path)
        return "\n".join(p.text for p in doc.paragraphs)
    # fallback: try to decode file bytes
    with open(path, "rb") as f:
        return f.read().decode("utf-8", errors="ignore")


# Chunking

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Simple char-based chunking with overlap."""
    if not text:
        return []
    chunks = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + chunk_size, n)
        chunks.append(text[start:end].strip())
        # move window forward
        start = end - overlap
        if start < 0:
            start = 0
        if start >= n:
            break
    # drop empty
    return [c for c in chunks if c]