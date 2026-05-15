# AI Customer Support Chatbot

An AI-powered customer support chatbot prototype utilizing Retrieval-Augmented Generation (RAG) to answer questions based on company FAQ documents. 

## Features
- **RAG Implementation**: Upload PDFs to build a vector knowledge base.
- **Conversational Memory**: Chatbot remembers context from previous turns in the conversation.
- **Fallback Responses**: Gracefully handles out-of-context or off-topic questions.
- **Modern UI**: Streamlit frontend for easy interaction.
- **Robust API**: FastAPI backend powering the logic.

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

## API Flow Documentation

### `POST /upload`
- **Description**: Accepts a PDF file, extracts text, chunks it, generates embeddings using `OpenAIEmbeddings`, and stores it in a local FAISS vector database.
- **Input**: `multipart/form-data` with a `file` field.
- **Output**: Success or error message.

### `POST /chat`
- **Description**: Accepts a user query and the chat history. Retrieves the top 3 most relevant context chunks from FAISS, injects them into a LangChain conversational prompt, and queries GPT-4o-mini to generate a response.
- **Input**: JSON payload containing `message` (string) and `history` (list of role/content objects).
- **Output**: JSON payload with `reply`.
<img width="1896" height="807" alt="Image" src="https://github.com/user-attachments/assets/655803e7-58fe-4800-bdf9-4f1fa3289de7" />

<img width="1906" height="822" alt="Image" src="https://github.com/user-attachments/assets/96f343f8-3f0c-47d5-bdce-e56d01e864d6" />
### `GET /health`
- **Description**: Simple health check endpoint.
