# app/hfclient.py
import os
import requests

HF_API_KEY = os.getenv("HF_API_KEY", "")
HF_EMBED_MODEL = os.getenv("HF_EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
HF_GEN_MODEL = os.getenv("HF_GEN_MODEL", "google/flan-t5-base")  # adjust to a generation-capable model

HF_HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"} if HF_API_KEY else {}

def hf_embed(text):
    """
    Call HF Inference API to get embedding (returns list[float]).
    """
    url = f"https://api-inference.huggingface.co/models/{HF_EMBED_MODEL}"
    payload = {"inputs": text}
    resp = requests.post(url, headers=HF_HEADERS, json=payload, timeout=30)
    resp.raise_for_status()
    # Many sentence-transformer models return {"embedding": [...] } or directly list.
    data = resp.json()
    if isinstance(data, dict) and "embedding" in data:
        return data["embedding"]
    # sometimes returns list
    if isinstance(data, list) and all(isinstance(x, (int, float)) for x in data):
        return data
    # if the model returns other shapes, raise
    raise RuntimeError("Unexpected embedding response: {}".format(data))

def hf_generate(prompt, max_length=256):
    """
    Call HF Inference API for text generation. Returns the generated text.
    """
    url = f"https://api-inference.huggingface.co/models/{HF_GEN_MODEL}"
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": max_length}}
    resp = requests.post(url, headers=HF_HEADERS, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    # Many generation models return [{'generated_text': '...'}]
    if isinstance(data, list) and data and isinstance(data[0], dict) and "generated_text" in data[0]:
        return data[0]["generated_text"]
    # some return string
    if isinstance(data, dict) and "generated_text" in data:
        return data["generated_text"]
    if isinstance(data, str):
        return data
    raise RuntimeError("Unexpected generation response: {}".format(data))