# from core.rag_gfg import rag_from_gfg

# def smart_rag(query):
#     return rag_from_gfg(query)  # Add fallback to notes later if needed


# # ✅ FILE: app.py
# # Streamlit app UI
# import streamlit as st
# from core.smart_rag import smart_rag

# st.set_page_config(page_title="DSA RAG Chatbot")
# st.title("🤖 Ask Me Anything About DSA")

# query = st.text_input("Your DSA question:")
# if query:
#     with st.spinner("Thinking..."):
#         answer = smart_rag(query)
#         st.markdown(f"**Answer:**\n\n{answer}")

from core.rag_gfg import rag_from_gfg
from core.rag_notes import rag_from_notes

def smart_rag(query):
    gfg_answer = rag_from_gfg(query)

    # If the answer is a generator (streaming), collect it
    if hasattr(gfg_answer, '__iter__') and not isinstance(gfg_answer, str):
        gfg_answer_text = "".join(list(gfg_answer)).strip()
        if "⚠️" in gfg_answer_text or len(gfg_answer_text) < 50:
            print("🔁 Falling back to local notes...")
            return rag_from_notes(query)
        return gfg_answer_text
    else:
        if "⚠️" in gfg_answer or len(gfg_answer.strip()) < 50:
            print("🔁 Falling back to local notes...")
            return rag_from_notes(query)
        return gfg_answer
