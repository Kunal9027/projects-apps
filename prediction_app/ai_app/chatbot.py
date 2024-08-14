from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
MODEL_NAME = "mixtral-8x7b-32768"

def chef(text):
    chat = ChatGroq(temperature=0, groq_api_key=API_KEY, model_name=MODEL_NAME)
    
    system_message ="You are a world-class chef with a vast knowledge of recipes. Respond to users' queries with clear, concise, and easy-to-follow cooking instructions. Keep your answers brief, under 200 words. If a user asks about a topic unrelated to cooking or food, respond with: 'I am a chef, I only know about cooking and food recipes.' Focus on providing helpful and accurate information to assist users in cooking delicious meals."
    
    human_message = text
    
    prompt = ChatPromptTemplate.from_messages([("system", system_message), ("human", human_message)])
    
    chain = prompt | chat
    
    result = chain.invoke({"text": text})
    
    return result.content

