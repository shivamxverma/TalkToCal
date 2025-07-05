from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from utils import check_availability, book_event
import os
from dotenv import load_dotenv
load_dotenv()


llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), temperature=0)

tools = [
    Tool(name="check_availability", func=check_availability, description="Check available slots"),
    Tool(name="book_event", func=book_event, description="Book an event"),
]

agent = initialize_agent(tools, llm, agent_type="zero-shot-react-description")

def handle_message(msg: str):
    return agent.run(msg)
