# ragg


## run (step-by-step)
1. create the project files
2. Copy .env.ex to .env and set HF_API_KEY.
3. Create Python venv and install deps:

    python -m venv .venv
    venv\Scripts\activate    
    pip install -r requirements.txt
    pip install streamlit

📌 AI Chatbot with Document Upload (FastAPI + Streamlit + LangChain + Hugging Face)

This project implements a simple AI chatbot that allows users to upload multiple PDF (or text/docx) documents, extracts text, generates embeddings, stores metadata in a SQL database, and answers user queries using a RAG (Retrieval-Augmented Generation) pipeline.
```bash
📂 Project Structure
ragg/
├── app/                    
│    ├── config.py           # configuration
│    ├── db.py               # database config
│    ├── embeddings.py       # LangChain Embeddings wrapper
│    ├── hfclient.py         # HF Inference API calls
│    ├── main.py             # FastAPI app
│    ├── models.py           # schema
│    ├── rag.py              # ingestion + storage + vector store
│    ├── schemas.py          # FastAPI server
├── tests/                  
│    ├── test_api.py         # testing
├──  streamlit_app.py        # Streamlit frontend       
├── README.md                # Project documentation
├──  requirements            # Python dependencies
├──  .env                    # Environment variables ( API keys)

```


