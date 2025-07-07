from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain.llms import Ollama

# Load local vector store
retriever = Chroma(
    persist_directory="db",
    embedding_function=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
).as_retriever()

# Define Ollama LLM (wraps local mistral)
llm = Ollama(model="tinyllama")


# Build RAG pipeline over your notes
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=False
)

def rag_from_notes(query):
    return qa_chain.run(query)
