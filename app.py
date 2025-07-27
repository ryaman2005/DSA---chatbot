# app.py
import streamlit as st
import base64
from core.smart_rag import get_final_response

st.set_page_config(page_title="DSA RAG Chatbot", layout="wide")

# ---- Custom CSS Styling ----
st.markdown("""
    <style>
    body {
        background: linear-gradient(-45deg, #0f2027, #203a43, #2c5364, #0f2027);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    section[data-testid="stSidebar"] {
        background: rgba(30, 30, 30, 0.8);
        backdrop-filter: blur(10px);
        border-right: 1px solid #444;
    }
    .chat-title {
        font-size: 3rem;
        font-weight: 900;
        color: white;
        text-shadow: 0 0 20px #00f0ff;
        animation: pulseText 3s infinite;
    }
    @keyframes pulseText {
        0% { text-shadow: 0 0 5px #00f0ff; }
        50% { text-shadow: 0 0 25px #00f0ff; }
        100% { text-shadow: 0 0 5px #00f0ff; }
    }
    .stTextInput > div > div > input {
        background-color: #111 !important;
        color: #fff !important;
        border: 1px solid #444;
        border-radius: 8px;
    }
    .stMarkdown {
        font-family: 'Fira Code', monospace;
        color: #ddd;
        font-size: 1.1rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='chat-title'>DSA RAG Chatbot</div>", unsafe_allow_html=True)

# Sidebar Markdown Editor
st.sidebar.title("📝 Notes")
show_editor = st.sidebar.checkbox("Show Markdown Editor")

if show_editor:
    editor_content = st.text_area("Write your DSA notes here:", height=200)
    if st.button("💾 Export Notes"):
        b64 = base64.b64encode(editor_content.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="dsa_notes.md">📥 Download Markdown</a>'
        st.markdown(href, unsafe_allow_html=True)

# Main Chat Section
query = st.text_input("Ask a question about DSA:")

if query:
    with st.spinner("🔍 Thinking..."):
        response = get_final_response(query)

    st.markdown("### 💡 Response:")
    if "```" in response:
        lines = response.split("\n")
        in_code_block = False
        code_lines = []
        for line in lines:
            if line.strip().startswith("```"):
                if in_code_block:
                    st.code("\n".join(code_lines), language="python")
                    code_lines = []
                in_code_block = not in_code_block
            elif in_code_block:
                code_lines.append(line)
            else:
                st.markdown(line)
    else:
        st.markdown(response)
