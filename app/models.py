#app/models.py
from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    original_filename = Column(String, nullable=False)
    stored_filename = Column(String, nullable=False)
    upload_ts = Column(DateTime, default=datetime.utcnow)
    text_length = Column(Integer, default=0)
    # relationship to chunks
    chunks = relationship("Chunk", back_populates="file", cascade="all, delete-orphan")

class Chunk(Base):
    __tablename__ = "chunks"
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("files.id"), nullable=False)
    chunk_text = Column(String, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    embedding = Column(LargeBinary, nullable=False)  # store numpy array bytes
    meta = Column(JSON, nullable=True)
    file = relationship("File", back_populates="chunks")