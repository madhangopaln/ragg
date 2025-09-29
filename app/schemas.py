# app/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class FileOut(BaseModel):
    id: int
    original_filename: str
    stored_filename: str
    upload_ts: datetime
    text_length: int

    class Config:
        orm_mode = True

class ChatRequest(BaseModel):
    question: str
    top_k: int = 3

class ChatResponse(BaseModel):
    answer: str
    used_chunks: List[str]