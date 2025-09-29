# streamlit_app.py
import streamlit as st
import requests
import os

API_BASE = os.getenv("API_BASE", "http://localhost:8000")

st.title("Simple RAG Chat (PDFs)")

st.subheader("Upload PDF files")
uploaded = st.file_uploader("Select PDF files", type=["pdf"], accept_multiple_files=True)
if uploaded and st.button("Upload"):
    for f in uploaded:
        files = {"files": (f.name, f.getvalue(), "application/pdf")}
        resp = requests.post(f"{API_BASE}/upload", files=files)
        if resp.ok:
            st.success(f"Uploaded {f.name}")
        else:
            st.error(f"Failed {f.name}: {resp.text}")

st.subheader("Ask a question")
q = st.text_area("Your question")
k = st.slider("Top-k chunks", 1, 5, 3)
if st.button("Ask"):
    resp = requests.post(f"{API_BASE}/chat", json={"question": q, "top_k": k})
    if resp.ok:
        j = resp.json()
        st.markdown("**Answer:**")
        st.write(j["answer"])
        st.markdown("**Used file IDs:**")
        st.write(j["used_ids"])
    else:
        st.error("Chat failed: " + resp.text)

st.markdown("---")
if st.button("List files on server"):
    r = requests.get(f"{API_BASE}/files")
    if r.ok:
        for f in r.json():
            st.write(f"- {f['id']}: {f['original_filename']} (len={f['text_length']})")
    else:
        st.error("Could not fetch files")