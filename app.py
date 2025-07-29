# app.py

import streamlit as st
import base64
import time
import os
from core.smart_rag import get_final_response, process_and_store_documents, get_vector_store # Updated imports

st.set_page_config(page_title="HEK", layout="wide", page_icon="🤖")

# --- Configuration (Centralized in app.py for easy management) ---
# Directory to store uploaded files temporarily for processing
UPLOAD_DIR = "uploaded_docs"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Directory for ChromaDB persistence - MUST match your folder structure
CHROMA_PERSIST_DIR = "db" # <--- IMPORTANT: Changed this to "db" to match your structure
if not os.path.exists(CHROMA_PERSIST_DIR):
    os.makedirs(CHROMA_PERSIST_DIR)

# Ollama Models
LLM_MODEL = "mistral" # Or your preferred LLM
EMBEDDING_MODEL = "nomic-embed-text" # A good local embedding model

# --- Session State Initialization ---
if "page" not in st.session_state:
    st.session_state.page = "intro"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
# The rag_processed flag is now more dynamic, based on actual DB content,
# but can still be useful to guide UI messages.
# Initialize the vector store early to benefit from caching and check existence.
st.session_state.vectorstore = get_vector_store(CHROMA_PERSIST_DIR, EMBEDDING_MODEL)


# ---- Intro animation screen ----
if st.session_state.page == "intro":
    st.markdown("""
        <style>
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(120deg, #0f2027, #203a43, #2c5364);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
            color: #f0f0f0;
            text-align: center;
        }
        @keyframes gradientBG {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
        .intro-logo {
            font-size: 5rem;
            font-weight: bold;
            margin-top: 25vh;
            color: #00f0ff;
            animation: pulse 2s ease-in-out infinite;
            text-shadow: 0 0 20px #00f0ff;
        }
        @keyframes pulse {
            0% {transform: scale(1);}
            50% {transform: scale(1.1);}
            100% {transform: scale(1);}
        }
        </style>
        <div class="intro-logo">HEK</div>
    """, unsafe_allow_html=True)

    # Auto-switch after delay
    time.sleep(3)
    st.session_state.page = "chat"
    st.rerun()


# ---- Main Chatbot Page ----
elif st.session_state.page == "chat":
    # Your existing CSS styles
    st.markdown("""
        <style>
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(120deg, #0f2027, #203a43, #2c5364);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
            color: #f0f0f0;
        }
        @keyframes gradientBG {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
        section[data-testid="stSidebar"] {
            background: rgba(30, 30, 30, 0.6);
            border-right: 1px solid #444;
            backdrop-filter: blur(12px);
        }
        .chat-title {
            font-size: 3rem;
            font-weight: bold;
            color: #00f0ff;
            text-align: center;
            margin: 30px 0;
            text-shadow: 0 0 15px #00f0ff;
            animation: glow 2s ease-in-out infinite alternate;
        }
        @keyframes glow {
            from { text-shadow: 0 0 10px #00f0ff; }
            to { text-shadow: 0 0 25px #00f0ff; }
        }
        .stTextInput > div > div > input {
            background-color: #111 !important;
            color: #eee !important;
            border: 1px solid #555;
            border-radius: 10px;
            padding: 10px;
            font-size: 1rem;
        }
        .stMarkdown {
            font-family: 'Fira Code', monospace;
            color: #f8f8f8;
        }
        .response-block {
            background: rgba(255, 255, 255, 0.05);
            padding: 1.2rem;
            border-radius: 10px;
            margin-top: 20px;
        }
        .markdown-editor {
            background-color: #1e1e1e;
            color: #ddd;
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)

    # ---- App Title ----
    st.markdown("<div class='chat-title'> HEK </div>", unsafe_allow_html=True)

    # ---- Sidebar: Manage Knowledge Base ----
    with st.sidebar:
        st.header("📚 Knowledge Base")
        st.subheader("Add Documents")
        uploaded_files = st.file_uploader(
            "Upload your notes (PDF, TXT, MD)", # Remind user about supported types
            type=["pdf", "txt", "md"],
            accept_multiple_files=True,
            key="kb_uploader"
        )

        if uploaded_files:
            if st.button("Process & Update KB"):
                with st.spinner("Processing documents..."):
                    # Call the function from smart_rag.py
                    processed_vectorstore = process_and_store_documents(
                        uploaded_files, UPLOAD_DIR, CHROMA_PERSIST_DIR, EMBEDDING_MODEL
                    )
                    # Update the cached vectorstore in session_state if processing was successful
                    if processed_vectorstore:
                        st.session_state.vectorstore = processed_vectorstore
                        st.rerun() # Rerun to update the info message and chat state

        # Display current status of KB
        # Check if the persisted directory exists and has contents
        kb_is_populated = os.path.exists(CHROMA_PERSIST_DIR) and len(os.listdir(CHROMA_PERSIST_DIR)) > 0
        
        if kb_is_populated:
            st.success("Knowledge Base is ready for RAG. You can ask questions based on your documents.")
        else:
            st.warning("Knowledge Base is empty. Upload documents above to enable RAG.")

        st.markdown("---") # Separator

    # ---- Sidebar Notes Editor (Your existing code) ----
    st.sidebar.header(" Notes")
    if st.sidebar.checkbox("Show Markdown Editor"):
        editor_content = st.text_area("Write your DSA notes here:", height=200, key="notes", placeholder="Write markdown notes here...", help="Write your DSA-related notes.")
        if st.button(" Export Notes"):
            b64 = base64.b64encode(editor_content.encode()).decode()
            href = f'<a href="data:file/txt;base64,{b64}" download="dsa_notes.md">📥 Download Markdown</a>'
            st.markdown(href, unsafe_allow_html=True)

    # ---- Main Chat Interface ----
    # Display chat history (adjusted for proper message display and sources)
    for pair in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(pair["question"])
        with st.chat_message("assistant"):
            st.markdown(pair["answer"])
            if pair.get("sources"):
                with st.expander("Show Sources"):
                    for source in pair["sources"]:
                        # Ensure 'source' metadata exists or default to 'N/A'
                        # Use a monospaced font for code snippets
                        st.markdown(f"- **Source:** `{source.metadata.get('source', 'N/A')}`")
                        st.markdown(f"  **Snippet:** ```\n{source.page_content[:200]}...\n```") # Show first 200 chars

    # Chat Input
    query = st.chat_input("Ask a question about DSA from your knowledge base:")

    if query:
        # Add user query to chat history display immediately
        with st.chat_message("user"):
            st.markdown(query)

        with st.spinner("🔍 Thinking..."):
            # Call the get_final_response function, passing necessary configs
            response_data = get_final_response(query, CHROMA_PERSIST_DIR, LLM_MODEL, EMBEDDING_MODEL)
            assistant_response = response_data["response"]
            source_documents = response_data.get("source_documents", []) # Get sources if returned

        # Add assistant response to chat history display
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
            if source_documents:
                with st.expander("Show Sources"):
                    for doc in source_documents:
                        st.markdown(f"- **Source:** `{doc.metadata.get('source', 'N/A')}`")
                        st.markdown(f"  **Snippet:** ```\n{doc.page_content[:200]}...\n```") # Show first 200 chars

        # Store full pair in session state including sources for history
        st.session_state.chat_history.append({
            "question": query,
            "answer": assistant_response,
            "sources": source_documents
        })
        # st.rerun() # Optional: reruns the app to make the latest chat visible immediately

    # Sidebar: Searchable Chat History (Your existing code)
    with st.sidebar:
        st.markdown("---")
        st.subheader("Chat History")
        search_term = st.text_input("Search past questions", key="history_search")

        displayed_history = []
        for pair in reversed(st.session_state.chat_history):
            if search_term.lower() in pair["question"].lower():
                displayed_history.append(pair)
        
        for pair in displayed_history:
            st.markdown(f"**You:** {pair['question']}")
            st.markdown(f"**HEK:** {pair['answer']}")
            if pair.get("sources"):
                st.markdown("**(Sources available - expand in main chat to view)**")
            st.markdown("---")

    # Optional: Clear chat history button
    if st.sidebar.button("Clear Chat History", key="clear_chat_button"):
        st.session_state.chat_history = []
        st.rerun()