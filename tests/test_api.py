# tests/test_api.py
import tempfile, os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import models
from app.db import engine
import app.hfclient as hf_client

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    yield

def dummy_embed(text):
    # deterministic small vector
    return [0.01] * 384

def dummy_generate(prompt, max_new_tokens=150):
    return "MOCKED ANSWER"

def test_upload_and_list(monkeypatch):
    monkeypatch.setattr(hf_client, "hf_embed", dummy_embed_embed)
    monkeypatch.setattr(hf_client, "hf_generate", dummy_generate)

    # create a small pdf file
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tmp.close()
    # write a minimal PDF stream (PyPDF2 can still fail on malformed PDF)
    # For simplicity, create a text file and pretend it's PDF for this unit test
    with open(tmp.name, "wb") as f:
        f.write(b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\ntrailer\n<<>>\n%%EOF")
    with open(tmp.name, "rb") as f:
        files = [("files", (os.path.basename(tmp.name), f, "application/pdf"))]
        r = client.post("/upload", files=files)
    os.unlink(tmp.name)
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert data[0]["original_filename"].endswith(".pdf")

    # list files
    r2 = client.get("/files")
    assert r2.status_code == 200
    assert len(r2.json()) >= 1

def test_chat_no_docs(monkeypatch):
    monkeypatch.setattr(hf_client, "hf_embed", dummy_embed)
    monkeypatch.setattr(hf_client, "hf_generate", dummy_generate)
    r = client.post("/chat", json={"question": "Hello", "top_k": 2})
    assert r.status_code == 200
    j = r.json()
    # when no docs, will reply "No documents uploaded yet."
    assert "No documents" in j["answer"] or j["answer"] == "MOCKED ANSWER"
