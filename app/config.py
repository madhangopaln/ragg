# app/config.py

from dotenv import load_dotenv
import os

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
HF_EMBED_MODEL = os.getenv("HF_EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
HF_GEN_MODEL = os.getenv("HF_GEN_MODEL", "google/flan-t5-base")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ragg_simple.db")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")