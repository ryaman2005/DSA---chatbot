# app.py
import streamlit as st
import base64
from core.smart_rag import get_final_response

st.set_page_config(page_title="HEK ", layout="wide", page_icon="🤖")

# ---- Custom CSS Styling ----
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

# ---- Sidebar Notes Editor ----
st.sidebar.header("📝 Notes")
if st.sidebar.checkbox("Show Markdown Editor"):
    editor_content = st.text_area("Write your DSA notes here:", height=200, key="notes", placeholder="Write markdown notes here...", help="Write your DSA-related notes.")
    if st.button("💾 Export Notes"):
        b64 = base64.b64encode(editor_content.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="dsa_notes.md">📥 Download Markdown</a>'
        st.markdown(href, unsafe_allow_html=True)

# ---- Main Chat Interface ----
query = st.text_input("Ask a question about DSA:")

if query:
    with st.spinner("🔍 Thinking..."):
        response = get_final_response(query)

    st.markdown("### 💡 Response:")
    st.markdown("<div class='response-block'>", unsafe_allow_html=True)

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

    st.markdown("</div>", unsafe_allow_html=True)

