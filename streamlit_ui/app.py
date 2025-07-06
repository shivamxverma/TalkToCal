import streamlit as st
import requests
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
import json
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

try:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  
except KeyError:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
    if not GEMINI_API_KEY:
        st.error("Gemini API key not found. Set it in secrets.toml or as an environment variable.")
        st.stop()

# Configure Gemini API

# print("Configuring Gemini API...")

# print("GEMINI_API_KEY:", os.getenv("GEMINI_API_KEY"))

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-pro")
chat = model.start_chat(history=[])

st.set_page_config(page_title="Calendar Booking Assistant", page_icon="📅")
st.title("📅 Scalable Appointment Booking Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm here to help you book an appointment. What would you like to do (e.g., check availability, book appointment)?"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Type your message...")
if user_input:
    print("User input received:", user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="Extract intent, date, time, duration, description from the following input. Return the result as a JSON object."),
            HumanMessage(content=user_input)
        ])
        
        messages = [
            {"role": "system", "content": prompt.messages[0].content},
            {"role": "user", "content": prompt.messages[1].content}
        ]
        
        response = chat.send_message(messages[1]["content"])  
        # print("Response from Gemini API:", response.text)
        parsed_text = response.text  
        print("Parsed response text:", parsed_text)
        
        # try:
        #     parsed = json.loads(parsed_text)
        # except json.JSONDecodeError:
        #     st.session_state.messages.append({"role": "assistant", "content": "Error: Invalid response format from Gemini API."})
        #     st.stop()

        st.write("Parsed JSON:", json.loads(parsed_text))
        

        res = requests.post("http://localhost:8000/appointment", json=json.loads(parsed_text))
        res.raise_for_status()
        api_response = res.json()
        
        print("API response:", api_response)

        # Append API response to chat
        st.session_state.messages.append({"role": "assistant", "content": api_response["message"]})

        # Display available slots if present
        if api_response.get("available_slots"):
            slot_msg = "Available slots: " + ", ".join(api_response["available_slots"][:3])
            st.session_state.messages.append({"role": "assistant", "content": slot_msg})

    except requests.exceptions.RequestException as e:
        st.session_state.messages.append({"role": "assistant", "content": f"Error: Could not process request. {str(e)}"})
    except Exception as e:
        st.session_state.messages.append({"role": "assistant", "content": f"Error with Gemini API: {str(e)}"})
