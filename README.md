# ragg


## run (step-by-step)
1. create the project files
2. Copy .env.ex to .env and set HF_API_KEY.
3. Create Python venv and install deps:

    python -m venv .venv
    venv\Scripts\activate    
    pip install -r requirements.txt
    pip install streamlit

📂 Project Structure
ragg/
├── app/                    
│    ├── config.py            # configuration
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




📌 AI Chatbot with Document Upload (FastAPI + Streamlit + LangChain + Hugging Face)

This project implements a simple AI chatbot that allows users to upload multiple PDF (or text/docx) documents, extracts text, generates embeddings, stores metadata in a SQL database, and answers user queries using a RAG (Retrieval-Augmented Generation) pipeline.
```bash

📂 Project Structure
ai-chatbot/
│── README.md                # Project documentation (this file)
│── requirements.txt          # Python dependencies
│── .env                      # Environment variables (HF token, DB URL, etc.)
│── docker-compose.yml        # For local deployment
│── Dockerfile                # Container setup
│
├── backend/                  # FastAPI backend
│   ├── main.py               # FastAPI entry point
│   ├── database.py           # SQLAlchemy DB connection
│   ├── models.py             # SQLAlchemy models (File, Chunk)
│   ├── rag.py                # RAG pipeline (chunking, embeddings, retrieval, generation)
│   ├── hf_client.py          # Hugging Face API client (embedding + generation calls)
│   ├── tests/                # Unit & integration tests
│   │   ├── test_api.py       # Tests for FastAPI endpoints
│   │   └── test_rag.py       # Tests for RAG pipeline
│   └── uploads/              # Uploaded documents (saved on server)
│
├── frontend/                 # Streamlit frontend
│   └── app.py                # Streamlit UI (file upload + chat interface)
│
└── migrations/ (optional)    # Alembic migrations if using for DB schema versioning
```

🚀 How It Works

Upload PDFs → Extract text with PyPDF2/docx/txt parsing.

Chunking → Split documents into overlapping text chunks.

Embeddings → Create embeddings using Hugging Face models (sentence-transformers).

Database → Save file metadata + embeddings with SQLAlchemy (SQLite by default).

Query → Retrieve most relevant chunks with cosine similarity.

RAG pipeline → Generate answers with Hugging Face text generation model.

Frontend → Streamlit app provides an easy-to-use UI.

🛠️ Setup in VS Code

Clone the repo:

git clone https://github.com/yourusername/ai-chatbot.git
cd ai-chatbot


Create a virtual environment:

python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows


Install dependencies:

pip install -r requirements.txt


Configure .env file:

HF_TOKEN=your_huggingface_api_key
DATABASE_URL=sqlite:///./backend/files.db


Run FastAPI backend:

uvicorn backend.main:app --reload


Run Streamlit frontend:

streamlit run frontend/app.py


Open:

Backend API docs → http://127.0.0.1:8000/docs

Streamlit UI → http://localhost:8501

🧪 Testing

Run all unit tests with:

pytest backend/tests/ -v

🐳 Docker Deployment
docker-compose up --build


This will start both FastAPI and Streamlit services in containers.


