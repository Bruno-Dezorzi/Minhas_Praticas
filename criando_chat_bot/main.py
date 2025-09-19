import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st

load_dotenv()
API_KEY = os.getenv("API_KEY")
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Bem-vindo ao Chat Bot com Gemini")

prompt = st.chat_input("Digite sua mensagem...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = st.session_state.chat.send_message(prompt)
    st.session_state.messages.append({"role": "bot", "content": response.text})

with st.container():
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f"""
                <div style="
                    text-align: right;
                    margin: 8px 0;
                ">
                    <div style="
                        display: inline-block;
                        background-color: #DCF8C6;
                        color: black;
                        padding: 10px 14px;
                        border-radius: 12px;
                        max-width: 70%;
                        word-wrap: break-word;
                        box-shadow: 1px 1px 4px rgba(0,0,0,0.2);
                    ">
                        {msg['content']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div style="
                    text-align: left;
                    margin: 8px 0;
                ">
                    <div style="
                        display: inline-block;
                        background-color: #F1F0F0;
                        color: black;
                        padding: 10px 14px;
                        border-radius: 12px;
                        max-width: 70%;
                        word-wrap: break-word;
                        box-shadow: 1px 1px 4px rgba(0,0,0,0.2);
                    ">
                        {msg['content']}
                """,
                unsafe_allow_html=True,
            )
