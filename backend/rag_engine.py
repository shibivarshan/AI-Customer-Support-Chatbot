import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# Define embeddings - using OpenAI embeddings
def get_embeddings():
    return OpenAIEmbeddings()

def get_llm():
    return ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

def load_and_process_document(file_path: str, vector_store_path: str = "vectorstore"):
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = text_splitter.split_documents(documents)

    embeddings = get_embeddings()
    
    # Store in FAISS
    vectorstore = FAISS.from_documents(splits, embeddings)
    vectorstore.save_local(vector_store_path)
    
    return True

def get_retriever(vector_store_path: str = "vectorstore"):
    if not os.path.exists(vector_store_path):
        return None
    embeddings = get_embeddings()
    vectorstore = FAISS.load_local(vector_store_path, embeddings, allow_dangerous_deserialization=True)
    return vectorstore.as_retriever(search_kwargs={"k": 3})

def setup_rag_chain():
    llm = get_llm()
    
    # Setup prompt with conversational memory and fallback
    system_prompt = (
        "You are a helpful AI customer support assistant for a company. "
        "Use the provided context to answer the user's questions. "
        "If you don't know the answer or the question is unrelated to the context, "
        "politely state that you don't have that information and offer to connect them with a human representative. "
        "Keep your answers clear, professional, and concise. "
        "\n\nContext:\n{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])
    
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    
    retriever = get_retriever()
    if retriever is None:
        return None
        
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    return rag_chain

def generate_response(question: str, chat_history: list):
    chain = setup_rag_chain()
    if chain is None:
        return "I'm sorry, I don't have any company documents loaded yet to answer your questions. Please upload a FAQ document first."
    
    # Format chat history for LangChain
    formatted_history = []
    for msg in chat_history:
        if msg["role"] == "user":
            formatted_history.append(HumanMessage(content=msg["content"]))
        else:
            formatted_history.append(AIMessage(content=msg["content"]))

    response = chain.invoke({"input": question, "chat_history": formatted_history})
    return response["answer"]
