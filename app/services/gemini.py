import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
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
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-pro")  # Use correct model name (updated from gemini-2.5-pro)
chat = model.start_chat(history=[])

async def extract_intent_from_user_input(message: str):
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="Parse the user's input to identify intent (check_availability, book_appointment, cancel_appointment) and extract date, time, duration, and description."),
        HumanMessage(content=message)
    ])
    response = await chat.send_message(
        messages=prompt.to_messages()
    )
    return json.loads(response.choices[0].message.content)
