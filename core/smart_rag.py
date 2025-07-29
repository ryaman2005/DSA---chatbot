# core/smart_rag.py

import os
import streamlit as st # Import st for displaying messages within the function
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama

# --- Configuration (Passed from app.py) ---
# We'll pass UPLOAD_DIR, CHROMA_PERSIST_DIR, LLM_MODEL, EMBEDDING_MODEL
# to these functions from app.py for centralized control.

# --- Helper Functions ---

def load_documents(file_path):
    """Loads documents based on file extension."""
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path)
    elif file_path.endswith(".md"):
        loader = UnstructuredMarkdownLoader(file_path)
    # Add more loaders for other file types as needed (e.g., CSV, DOCX)
    else:
        # Returning an empty list and letting the calling function handle warnings
        return []
    return loader.load()

# Using Streamlit's cache_resource for the vector store
# This ensures that the vector store is loaded/created only once per session
# and reused across app reruns, improving performance.
@st.cache_resource
def get_vector_store(chroma_persist_dir, embedding_model):
    """
    Initializes and returns the Chroma vector store.
    This function is cached to prevent re-loading the DB on every rerun.
    """
    embeddings = OllamaEmbeddings(model=embedding_model)
    # Ensure the directory exists before attempting to load
    if not os.path.exists(chroma_persist_dir) or not os.listdir(chroma_persist_dir):
        st.warning("ChromaDB directory is empty or does not exist. A new one will be created upon first document processing.")
        # Return an empty ChromaDB which will be populated by from_documents later
        return Chroma(embedding_function=embeddings, persist_directory=chroma_persist_dir)
    else:
        st.info("Loading existing Knowledge Base...")
        return Chroma(persist_directory=chroma_persist_dir, embedding_function=embeddings)

def process_and_store_documents(uploaded_files, upload_dir, chroma_persist_dir, embedding_model):
    """
    Processes uploaded files: loads, chunks, embeds, and stores in ChromaDB.
    This function will update the persistent ChromaDB.
    """
    all_documents = []
    for uploaded_file in uploaded_files:
        # Save the uploaded file temporarily
        file_path = os.path.join(upload_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.info(f"Loading {uploaded_file.name}...")
        documents = load_documents(file_path)
        if documents:
            all_documents.extend(documents)
        else:
            st.warning(f"Skipped unsupported file: {uploaded_file.name}")
        os.remove(file_path) # Clean up temporary file after loading

    if not all_documents:
        st.error("No supported documents found to process. Please upload PDF, TXT, or MD files.")
        return None # Indicate failure

    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(all_documents)
    
    # Get the cached vector store instance
    vectorstore = get_vector_store(chroma_persist_dir, embedding_model)

    # Add documents to the vector store. This will append new documents.
    st.info(f"Adding {len(chunks)} chunks to vector store... This might take a moment.")
    vectorstore.add_documents(chunks)
    vectorstore.persist() # Explicitly persist changes
    st.success(f"Knowledge base updated with {len(chunks)} new chunks!")
    return vectorstore # Return the updated vectorstore object

def get_final_response(query: str, chroma_persist_dir: str, llm_model: str, embedding_model: str):
    """
    Generates a response using RAG if documents are processed and DB exists,
    otherwise uses direct LLM.
    """
    llm = Ollama(model=llm_model)

    # Check if the ChromaDB directory actually contains data
    # os.listdir will be empty if only the directory exists but no data is persisted.
    chroma_db_exists_and_populated = os.path.exists(chroma_persist_dir) and len(os.listdir(chroma_persist_dir)) > 0

    if chroma_db_exists_and_populated:
        try:
            # Get the cached vector store instance
            vectorstore = get_vector_store(chroma_persist_dir, embedding_model)

            # Create retrieval QA chain
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=vectorstore.as_retriever(),
                return_source_documents=True # Crucial for showing sources
            )

            response = qa_chain.invoke({"query": query})
            return {
                "response": response["result"],
                "source_documents": response.get("source_documents", [])
            }
        except Exception as e:
            st.error(f"RAG system encountered an error: {e}. Falling back to general LLM response.")
            # In a real app, you'd log 'e' more robustly.
            return {
                "response": llm.invoke(query),
                "source_documents": []
            }
    else:
        # If no documents processed or DB doesn't exist, just use the LLM directly
        st.info("No knowledge base found/loaded. Answering with general LLM knowledge.")
        return {
            "response": llm.invoke(query),
            "source_documents": []
        }