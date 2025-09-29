# app/main.py

import os
from fastapi import FastAPI, UploadFile, File as UploadFileType, Depends, HTTPException
from fastapi.responses import HTMLResponse
from typing import List
from sqlalchemy.orm import Session
from .db import SessionLocal, engine
from . import models
from .schemas import FileOut, ChatRequest, ChatResponse
from .rag import store_file_and_chunks, answer_question
from .config import UPLOAD_DIR

# create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="RAG Chat Backend")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload", response_model=List[FileOut])
async def upload_files(files: List[UploadFileType] = UploadFileType(...), db: Session = Depends(get_db)):
    saved = []
    for up in files:
        stored_name = f"{int(__import__('time').time()*1000)}_{up.filename}"
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        stored_path = os.path.join(UPLOAD_DIR, stored_name)
        with open(stored_path, "wb") as f:
            content = await up.read()
            f.write(content)
        try:
            file_rec = store_file_and_chunks(db, stored_path, up.filename)
            saved.append(file_rec)
        except Exception as e:
            # cleanup if store fails
            if os.path.exists(stored_path):
                os.remove(stored_path)
            raise HTTPException(status_code=400, detail=str(e))
    return saved

@app.get("/files", response_model=List[FileOut])
def list_files(db: Session = Depends(get_db)):
    files = db.query(models.File).all()
    return files

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    res = answer_question(db, req.question, top_k=req.top_k)
    return ChatResponse(answer=res["answer"], used_chunks=res["used_chunks"])

@app.get("/", response_class=HTMLResponse)
def root():
    return HTMLResponse(content="<h2>RAG Chat Backend</h2><p>Endpoints: /upload (POST), /files (GET), /chat (POST)</p>")
