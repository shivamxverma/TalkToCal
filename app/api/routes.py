from fastapi import APIRouter
from app.models.schema import AppointmentRequest, AppointmentResponse
from app.models.state import AgentState
from app.core.langgraph import graph

router = APIRouter()

@router.post("/appointment", response_model=AppointmentResponse)
async def handle_appointment(request: AppointmentRequest):
    print("Received appointment request:", request)
    state = AgentState()
    state.messages = [{"role": "user", "content": f"Intent: {request.intent}, Date: {request.date}, Time: {request.time}, Duration: {request.duration}, Description: {request.description}"}]
    state.intent = request.intent
    state.date = request.date
    state.time = request.time
    state.duration = request.duration
    state.description = request.description

    final_state = await graph.ainvoke(state)
    return AppointmentResponse(
        message=final_state.messages[-1]["content"],
        available_slots=final_state.available_slots,
        booking_id=final_state.messages[-1]["content"].split("Event ID: ")[-1] if "Event ID" in final_state.messages[-1]["content"] else None
    )
