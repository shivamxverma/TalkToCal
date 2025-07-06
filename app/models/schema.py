from pydantic import BaseModel
from typing import List, Optional

class AppointmentRequest(BaseModel):
    intent: str
    date: Optional[str] = None
    time: Optional[str] = None
    duration: Optional[int] = None
    description: Optional[str] = None

class AppointmentResponse(BaseModel):
    message: str
    available_slots: Optional[List[str]] = None
    booking_id: Optional[str] = None
