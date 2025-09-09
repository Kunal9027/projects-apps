

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
import os, dotenv

dotenv.load_dotenv()
embedding_model = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

# def extract_text(pdf_path):
#     reader = PdfReader(pdf_path)
#     return " ".join([p.extract_text() for p in reader.pages if p.extract_text()])

# def setup_vector_db(pdf_text, chunk_size=700, chunk_overlap=200):
#     text = 
#     # print(text)
#     splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
#     docs = [Document(page_content=chunk) for chunk in splitter.split_text(text)]
#     return FAISS.from_documents(docs, embedding_model)
    

# Example
# vector_db = setup_vector_db("chat_bot/Resume.pdf")


# vector_db_openai1.py
# global_vector_dbs = {}

# def setup_vector_db(pdf_text, session_id, chunk_size=700, chunk_overlap=200):
#     splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
#     docs = [Document(page_content=chunk) for chunk in splitter.split_text(pdf_text)]
#     db = FAISS.from_documents(docs, embedding_model)
#     global_vector_dbs[session_id] = db
#     return db

# def get_vector_db(session_id):
#     return global_vector_dbs.get(session_id)

global_vector_dbs = {}


def setup_vector_db(pdf_text, session_id, chunk_size=700, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    docs = [Document(page_content=chunk) for chunk in splitter.split_text(pdf_text)]
    db = FAISS.from_documents(docs, embedding_model)
    # Clear all old DBs whenever a new session starts
    global_vector_dbs.clear()
    global_vector_dbs[session_id] = db
    return db


def get_vector_db(session_id):
    return global_vector_dbs.get(session_id)


def reset_vector_db(session_id):
    """Completely remove a session's vector DB (start fresh)."""
    if session_id in global_vector_dbs:
        del global_vector_dbs[session_id]
    return None
