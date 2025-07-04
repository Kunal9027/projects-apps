from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document
import json


question_answer_pairs = [
    {
      "question": "I have not received Rakuten Points for items that I have bought at Rakuten.",
      "answer": "In case of problems with orders or points on Rakuten, please contact Rakuten Customer Support here: https://www.rakuten.co.jp/help/. *Support is only in Japanese."
    },
    {
      "question": "I forgot my log-in ID and password. What should I do?",
      "answer": "You can reset your password from the Account Information Page of Rakuten Ichiba."
    },
    {
      "question": "Even though I already paid GST/VAT to Rakuten Global Express, I was asked to pay it again during import. What should I do?",
      "answer": "If you already paid GST to Rakuten Global Express but were re-invoiced, you can get a refund via your payment method, Japanese bank transfer, or Rakuten points. Submit your receipt and select 'duplicate GST/VAT payment'."
    }
  ]
  

# Load and embed Q&A once
# def setup_vector_db(path="data.json"):
def setup_vector_db(path=question_answer_pairs):
    # with open(path, "r", encoding="utf-8") as f:
    #     qa_data = json.load(f)
    
    qa_data = path

    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    docs = [Document(page_content=item["question"], metadata={"answer": item["answer"]}) for item in qa_data]

    vector_db = FAISS.from_documents(docs, embedding_model)
    return vector_db
