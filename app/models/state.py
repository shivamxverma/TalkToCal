from typing import List, Optional
import numpy as np

class AgentState:
    def __init__(self):
        self.messages: List[dict] = []
        self.intent: str = ""
        self.date: Optional[str] = None
        self.time: Optional[str] = None
        self.duration: Optional[int] = None
        self.description: Optional[str] = None
        self.available_slots: List[str] = []
        self.query_embedding: Optional[np.ndarray] = None
