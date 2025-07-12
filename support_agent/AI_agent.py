# from langchain_core.prompts import ChatPromptTemplate
# from langchain.schema import SystemMessage, HumanMessage
# from langchain.memory import ConversationBufferMemory
# from langchain.chains import LLMChain
# from langchain_groq import ChatGroq
# from vector_db import setup_vector_db
# import os
# import dotenv

# API_KEY = os.getenv('API_KEY')

# # Init Groq LLM
# llm = ChatGroq(
#     model="llama-3.3-70b-versatile",
#     temperature=0.0,
#     max_retries=1,
#     api_key=API_KEY
# )

# # Build once at startup
# vector_db = setup_vector_db()
# memory = ConversationBufferMemory(return_messages=True)

# #  Chat handler
# def chat_with_user(user_input):
#     results = vector_db.similarity_search(user_input, k=1)
#     if not results:
#         return "申し訳ありませんが、この質問の情報は見つかりませんでした。サポートチームにお問い合わせください。\nI'm sorry, I couldn't find an answer. Please contact our customer support team."

#     retrieved_q = results[0].page_content
#     retrieved_a = results[0].metadata["answer"]

#     #  Prompt Template
#     prompt = ChatPromptTemplate.from_messages([
#         ("system", f"""
# あなたは楽天のカスタマーサポート担当者です。以下のFAQに基づいて、ユーザーの質問に日本語と英語の両方で丁寧に答えてください。想像や仮定はせず、FAQにない場合はサポートチームへの連絡を促してください。

# Q: {retrieved_q}
# A: {retrieved_a}
# """),
#         ("human", "{input}")
#     ])

#     chain = LLMChain(llm=llm, prompt=prompt, memory=memory)
#     response = chain.invoke({"input": user_input})
#     return response["text"]


# #  Test (run this if running locally)
# if __name__ == "__main__":
#     print(" Ask me your Rakuten support question:")
#     while True:
#         query = input("You: ")
        
#         if query.lower() in ["exit", "quit", "bye" ,"q"]:
#             print(" Goodbye!")
#             break
        
#         reply = chat_with_user(query)
#         print("Bot:\n", reply)
        
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_groq import ChatGroq
# from vector_db import setup_vector_db
from .vector_db_openai import setup_vector_db
import os
import dotenv

dotenv.load_dotenv()
API_KEY = os.getenv('API_KEY')

#  Init Groq LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.0,
    max_retries=1,
    api_key=API_KEY
)

#  Build once at startup
vector_db = setup_vector_db()

#  In-memory message history store (for demo/testing)
history_store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in history_store:
        history_store[session_id] = ChatMessageHistory()
    return history_store[session_id]

#  Chat handler
def chat_with_user(user_input, session_id="user-1"):
    results = vector_db.similarity_search(user_input, k=1)
    if not results:
        return "申し訳ありませんが、この質問の情報は見つかりませんでした。サポートチームにお問い合わせください。\nI'm sorry, I couldn't find an answer. Please contact our customer support team."

    retrieved_q = results[0].page_content
    retrieved_a = results[0].metadata["answer"]

    #  Updated Prompt Template with memory placeholder
    prompt = ChatPromptTemplate.from_messages([
                    ("system", f"""
            Behave as customer support representative at Rakutenand your job is to help user with only rakuten service related issues.
            Please answer the user's questions politely, consise, quick to read and in the **same language** as the question, based on the FAQ provided below Please answer politely answer"
            If the question is in Japanese, respond in Japanese.  
            If the question is in English, respond in English.
            Do not make up answers. If the FAQ does not contain the answer, politely advise the user to contact the Rakuten support team or just say "I do not know the answer" but do not answer made up or other than faqs provided.
             FAQ
            Question: {retrieved_q}
            Answer: {retrieved_a}
            
            *and* format your responses using Markdown:
            - Use **bold** for key terms,
            - `inline code` for UI labels or commands,
            - Numbered lists for steps,
            - [Links](https://...) for URLs,
            - Blockquotes for warnings or notes.
            """),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])

    #  Chain with memory
    chain = prompt | llm

    chain_with_memory = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history"
    )

    response = chain_with_memory.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": session_id}}
    )
    print(response.content)
    return response.content


# 🧪 Test locally
if __name__ == "__main__":
    print("📩 Ask me your Rakuten support question:")
    while True:
        query = input("You: ")

        if query.lower() in ["exit", "quit", "bye", "q"]:
            print(" Goodbye!")
            break

        reply = chat_with_user(query, session_id="test-user")
        print("Bot:\n", reply)
