from langgraph.graph import StateGraph, END
from app.models.state import AgentState
from app.services.gemini import extract_intent_from_user_input
from app.core.calendar import get_calendar_service
from app.core.chroma import collection, embedding_function
from app.services.slot_utils import generate_time_slots
from datetime import datetime, timedelta

async def understand_intent(state: AgentState) -> AgentState:
    parsed = await extract_intent_from_user_input(state.messages[-1]["content"])
    state.intent = parsed.get("intent", "")
    state.date = parsed.get("date")
    state.time = parsed.get("time")
    state.duration = parsed.get("duration")
    state.description = parsed.get("description")
    query = f"{state.intent} {state.date or ''} {state.time or ''} {state.description or ''}"
    state.query_embedding = embedding_function([query])[0]
    return state

async def check_availability(state: AgentState) -> AgentState:
    if state.intent in ["check_availability", "book_appointment"]:
        service = get_calendar_service()
        start = datetime.strptime(state.date, "%Y-%m-%d") if state.date else datetime.now()
        end = start + timedelta(days=1)
        events = service.events().list(calendarId='primary', timeMin=start.isoformat()+'Z', timeMax=end.isoformat()+'Z', singleEvents=True, orderBy='startTime').execute().get('items', [])
        for event in events:
            event_text = f"{event.get('summary', '')} {event['start']['dateTime']} {event.get('description', '')}"
            collection.upsert(
                ids=[event['id']],
                documents=[event_text],
                metadatas=[{"start_time": event['start']['dateTime'], "end_time": event['end']['dateTime']}],
                embeddings=embedding_function([event_text])
            )
        results = collection.query(
            query_embeddings=[state.query_embedding],
            n_results=10,
            where={"start_time": {"$gte": start.isoformat(), "$lte": end.isoformat()}}
        )
        booked = [meta["start_time"] for meta in results["metadatas"][0]]
        state.available_slots = generate_time_slots(start, booked)
    return state

async def suggest_slots(state: AgentState) -> AgentState:
    msg = "Available slots: " + ", ".join(state.available_slots[:3]) if state.available_slots else "No slots available. Choose another date."
    state.messages.append({"role": "assistant", "content": msg})
    return state

async def book_appointment(state: AgentState) -> AgentState:
    if state.intent == "book_appointment" and state.time in state.available_slots:
        service = get_calendar_service()
        event = {
            'summary': state.description or 'Appointment',
            'start': {'dateTime': state.time, 'timeZone': 'UTC'},
            'end': {'dateTime': (datetime.fromisoformat(state.time) + timedelta(minutes=state.duration or 30)).isoformat(), 'timeZone': 'UTC'}
        }
        created = service.events().insert(calendarId='primary', body=event).execute()
        event_text = f"{created.get('summary', '')} {created['start']['dateTime']} {created.get('description', '')}"
        collection.upsert(ids=[created['id']], documents=[event_text], metadatas=[{"start_time": created['start']['dateTime'], "end_time": created['end']['dateTime']}], embeddings=embedding_function([event_text]))
        state.messages.append({"role": "assistant", "content": f"Appointment booked successfully! Event ID: {created['id']}"})
    else:
        state.messages.append({"role": "assistant", "content": "Please select a valid available time slot."})
    return state

workflow = StateGraph(AgentState)
workflow.add_node("understand_intent", understand_intent)
workflow.add_node("check_availability", check_availability)
workflow.add_node("suggest_slots", suggest_slots)
workflow.add_node("book_appointment", book_appointment)
workflow.add_edge("understand_intent", "check_availability")
workflow.add_edge("check_availability", "suggest_slots")
workflow.add_edge("suggest_slots", "book_appointment")
workflow.add_edge("book_appointment", END)
workflow.set_entry_point("understand_intent")
graph = workflow.compile()
