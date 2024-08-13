from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

API_KEY ="YOUR_API"
model_8b ="mixtral-8x7b-32768"

chat = ChatGroq(temperature=0, groq_api_key=API_KEY, model_name=model_8b)


system = "You are a world class chef and you know every recipie. you only answer if some one ask about related to cooking or food recipe . if some one ask about other things you will not answer just say i am a chef i only know about cooking and food recipe."

human = "{text}"
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

chain = prompt | chat
chain.invoke({"text": "Explain the importance of low latency LLMs."})




