# app/embeddings.py
from langchain.embeddings.base import Embeddings
from typing import List
from .hf_client import hf_embed

class HFInferenceEmbeddings(Embeddings):
    """LangChain Embeddings wrapper calling HF Inference API (hf_embed)."""

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [hf_embed(t) for t in texts]

    def embed_query(self, text: str) -> List[float]:
        return hf_embed(text)