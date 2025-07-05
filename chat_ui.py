import streamlit as st
import requests

st.title("🤖 Calendar Booking Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

msg = st.chat_input("Say something")

if msg:
    st.session_state.messages.append(("You", msg))
    res = requests.post("http://localhost:8000/chat", json={"message": msg})
    reply = res.json()["response"]
    st.session_state.messages.append(("Bot", reply))

for sender, text in st.session_state.messages:
    st.write(f"**{sender}:** {text}")
