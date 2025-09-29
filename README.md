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

## Setting Up the Environment
### 1. Create a Virtual Environment
virtual environment isolates project dependencies. can use ven
```bash
Using venv:
python -m venv venv
venv\Scripts\activate  
```
### 2. Install Required Dependencies
Navigate to your project directory and install dependencies:
```bash
With pip:
pip install -r requirements.txt
pip install streamlit
```
### 3.Configuring Environment Variables
To keep sensitive information like API keys secure, store them in a .env file. This file should not be committed to version control.
Create a .env file in your project root and add your OpenAI API key:
```bash
HF_API_KEY=your_api_key
```
### 4.Create uploads dir:
```bash
mkdir -p ./uploads
```
### 5.Start FastAPI backend (development):
```bash
uvicorn backend.app.main:app --reload
```
### 6.Start Streamlit UI (in another terminal):
```bash
export API_BASE=http://localhost:8000  
streamlit run streamlit_app.py
```
### 7.Open:
```bash
Streamlit UI: http://localhost:8501
FastAPI docs: http://localhost:8000/docs
```

### 8.Run tests:
```bash
pytest -q
```

