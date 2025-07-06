import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
import google.generativeai as genai  # Gemini client wrapper

async def extract_intent_from_user_input(message: str):
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="Parse the user's input to identify intent (check_availability, book_appointment, cancel_appointment) and extract date, time, duration, and description."),
        HumanMessage(content=message)
    ])
    response = await genai.chat(
        messages=prompt.to_messages()
    )
    return json.loads(response.choices[0].message.content)
