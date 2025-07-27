# DSA RAG Chatbot

This chatbot answers Data Structure questions using live content from GeeksforGeeks and OpenAI's GPT.

## 🔧 Setup
1. Clone the repo
2. Add your OpenAI key in `.env`
3. Run:
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```

## 📁 Folder Structure
- `scraping/` → Web scraper for GFG
- `core/` → GPT logic & RAG flows
- `data/` → Optional: upload your DSA notes/PDFs
- `db/` → Stores vector DB (if using custom notes)

## 🚀 Features
- ✅ Live GFG scraping
- ✅ GPT-3.5 based responses
- 🔜 Hybrid support for local notes (optional)
"""