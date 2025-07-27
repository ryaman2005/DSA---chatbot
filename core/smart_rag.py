import os
from core.llm_ollama import query_local_llm
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_final_response(query: str) -> str:
    if os.path.exists("uploaded_file_vectordb"):
        print("📂 Using uploaded file context...")
        vectordb = Chroma(persist_directory="uploaded_file_vectordb", embedding_function=embedding)
    else:
        print("🌐 Using default vectordb...")
        vectordb = Chroma(persist_directory="./vectordb", embedding_function=embedding)

    results = vectordb.similarity_search(query, k=4)
    context = "\n\n".join([r.page_content for r in results])

    prompt = f"""You are a helpful assistant for Data Structures and Algorithms.
Use the below context to answer the question.

Context:
{context}

Question:
{query}

Answer:"""

    return query_local_llm(prompt)
