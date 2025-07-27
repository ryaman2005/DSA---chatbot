from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter

DB_PATH = "db"
embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

def save_to_vectorstore(text, source="gfg"):
    texts = text_splitter.split_text(text)
    vectordb = Chroma.from_texts(texts, embedder, persist_directory=DB_PATH, collection_name=source)
    vectordb.persist()

def load_vectorstore(source):
    return Chroma(persist_directory=DB_PATH, embedding_function=embedder, collection_name=source)
