# chatbot.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv("API_KEY")

def prompt_gemini():
    chat = model.start_chat(history=[])
    prompt = input("Esperando o prompt: ")
    while prompt != "sair":
        response = chat.send_message(prompt)
        print(response.text)
        prompt = input("Esperando o prompt: ")

try:
    
    genai.configure(api_key=API_KEY)

    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt_gemini()
        
except Exception as e:
    print("Erro:", e)