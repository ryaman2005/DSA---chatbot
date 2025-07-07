from scraping.gfg_scraper import fetch_gfg_article
from core.llm_ollama import stream_ollama_response  # ← Make sure this matches your function name

def rag_from_gfg(query):
    context = fetch_gfg_article(query)[:1000]  # limit for speed
    prompt = f"""
You are a helpful DSA tutor.
Use the following context from GeeksforGeeks to answer the question clearly.

Context:
{context}

Question:
{query}
"""
    return stream_ollama_response(prompt)

