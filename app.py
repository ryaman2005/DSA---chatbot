# import streamlit as st
# from core.smart_rag import smart_rag

# st.set_page_config(page_title="DSA RAG Chatbot")
# st.title("💬 BOHRA's CHATWORLD")

# # Initialize chat history
# if "history" not in st.session_state:
#     st.session_state.history = []

# # Input box
# query = st.text_input("Ask me anything about DSA:")

# # When user presses 'Send'
# if st.button("Send"):
#     if query:
#         st.session_state.history.append(("You", query))

#         with st.spinner("Thinking..."):
#             response = smart_rag(query)

#         # Check if the response is a generator (streaming)
#         if hasattr(response, '__iter__') and not isinstance(response, str):
#             output_container = st.empty()
#             final_response = ""
#             for token in response:
#                 final_response += token
#                 output_container.markdown(f"**Bot:** {final_response}")
#             st.session_state.history.append(("Bot", final_response))
#         else:
#             st.markdown(f"**Bot:** {response}")
#             st.session_state.history.append(("Bot", response))

# # Display chat history
# for speaker, msg in st.session_state.history:
#     st.markdown(f"**{speaker}:** {msg}")
import streamlit as st
from core.smart_rag import smart_rag
import graphviz

st.set_page_config(page_title="DSA RAG Chatbot")
st.title("💬 BOHRA's CHATWORLD")

# 🔧 Visualizer: Stack

def render_stack(items):
    g = graphviz.Digraph()
    g.attr(rankdir="TB")  # Top to Bottom

    for i, val in enumerate(reversed(items)):
        label = f"{val} (Top)" if i == 0 else str(val)
        g.node(f"{i}", label, shape="box")

        if i > 0:
            g.edge(f"{i}", f"{i - 1}")

    return g

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Input box
query = st.text_input("Ask me anything about DSA:")

# When user presses 'Send'
if st.button("Send"):
    if query:
        st.session_state.history.append(("You", query))

        with st.spinner("Thinking..."):
            response = smart_rag(query)

        # Check if streaming response
        if hasattr(response, '__iter__') and not isinstance(response, str):
            output_container = st.empty()
            full_response = ""
            for token in response:
                full_response += token
                output_container.markdown(f"**Bot:** {full_response}")
            st.session_state.history.append(("Bot", full_response))
        else:
            st.markdown(f"**Bot:** {response}")
            st.session_state.history.append(("Bot", response))

        # 📊 Show Stack diagram if relevant
        if "stack" in query.lower():
            st.subheader("📊 Visual Representation of Stack")
            st.graphviz_chart(render_stack(["40", "30", "20", "10"]))

# Display chat history
for speaker, msg in st.session_state.history:
    st.markdown(f"**{speaker}:** {msg}")
