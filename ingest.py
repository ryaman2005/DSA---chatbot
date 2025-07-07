from pptx import Presentation
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

def extract_text_from_pptx(file_path):
    prs = Presentation(file_path)
    full_text = ""
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                full_text += shape.text + "\n"
    return full_text

def ingest_notes(pptx_path):
    raw_text = extract_text_from_pptx(pptx_path)
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.create_documents([raw_text])

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    Chroma.from_documents(docs, embedding=embeddings, persist_directory="db")
    print("✅ Notes ingested successfully!")

if __name__ == "__main__":
    ingest_notes("data/DSA_Notes.pptx")
