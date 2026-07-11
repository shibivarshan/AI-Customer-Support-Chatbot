# 🤖 AI Customer Support Chatbot

An AI-powered customer support chatbot built using Retrieval-Augmented Generation (RAG) to provide accurate, context-aware responses from company knowledge documents.

The system uses LLMs, vector search, and conversational memory to automate customer support interactions. 

## ✨ Features

- 📚 RAG-based knowledge retrieval from PDF documents
- 🧠 Conversational memory for maintaining chat context
- 🔍 Semantic search using vector embeddings
- 🛡️ Fallback handling for unknown queries
- ⚡ FastAPI backend architecture
- 🎨 Streamlit interactive frontend

## 🏗️ System Architecture

```text
User Query
      |
      ▼
Streamlit Frontend
      |
      ▼
FastAPI Backend
      |
      ▼
Query Embedding
      |
      ▼
FAISS / ChromaDB
      |
      ▼
Relevant Context Retrieval
      |
      ▼
LangChain RAG Pipeline
      |
      ▼
LLM (GPT)
      |
      ▼
AI Response
```
## Environment Setup

1. **Clone or Download the Repository**
2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure Environment Variables**:
   Create a `.env` file in the root of the project with your API keys.
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Running the Application Locally

You will need to run both the FastAPI backend and Streamlit frontend simultaneously.

1. **Start the Backend**:
   Run this from the project root directory:
   ```bash
   python -m uvicorn backend.main:app --reload --port 8000
   ```

2. **Start the Frontend**:
   In a new terminal window, run:
   ```bash
   python -m streamlit run frontend/app.py
   ```

## 🔌 API Flow Documentation

### `POST /upload`

**Purpose:**
Upload PDF documents and create a searchable knowledge base.

**Process:**
- Extract text
- Split text into chunks
- Generate embeddings
- Store embeddings in the FAISS vector database

**Input:**
- `multipart/form-data` with a `file` field

**Output:**
- Success or error message

---

### `POST /chat`

**Purpose:**
Generate AI responses based on the retrieved document context.

**Process:**
- Receive the user query
- Retrieve the most relevant context chunks
- Pass the retrieved context to a LangChain prompt
- Generate a response using GPT-4o-mini

**Input:**
- JSON payload containing:
  - `message` (string)
  - `history` (list of role/content objects)

**Output:**
- JSON response containing the AI-generated reply

 ## 🛠️ Technology Stack

**Backend**
- Python
- FastAPI

**Frontend**
- Streamlit

**Generative AI**
- LangChain
- OpenAI API
- GPT-4o-mini
- RAG

**Vector Database**
- FAISS

**Tools**
- Git
- Virtual Environment

## 📌 Future Improvements

- User authentication
- Multi-company knowledge bases
- Voice-based customer support
- Cloud deployment
- Analytics dashboard
   
<img width="1896" height="807" alt="Image" src="https://github.com/user-attachments/assets/655803e7-58fe-4800-bdf9-4f1fa3289de7" />

<img width="1906" height="822" alt="Image" src="https://github.com/user-attachments/assets/96f343f8-3f0c-47d5-bdce-e56d01e864d6" />
### `GET /health`
- **Description**: Simple health check endpoint.
