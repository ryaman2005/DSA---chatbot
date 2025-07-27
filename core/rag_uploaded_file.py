# core/rag_uploaded_file.py

import pickle
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_context_from_uploaded_file(query: str, k=4) -> str:
    with open("uploaded_file_context.pkl", "rb") as f:
        vectordb = pickle.load(f)
    results = vectordb.similarity_search(query, k=k)
    return "\n\n".join([r.page_content for r in results])
