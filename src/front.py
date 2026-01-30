from src.schema import RawInput, StandardEvent
from typing import List

def normalize(raw: RawInput) -> StandardEvent:
    """입력을 표준 이벤트로 변환"""
    return StandardEvent(
        source=raw.source,
        type=raw.type,
        timestamp=raw.timestamp,
        payload=raw.payload
    )

class FrontHierMemory:
    def __init__(self):
        self.hot: List[StandardEvent] = []
        self.warm: List[StandardEvent] = []
        self.cold: List[StandardEvent] = []
    
    def add(self, event: StandardEvent):
        self.hot.append(event)
        if len(self.hot) > 5:
            self.warm.append(self.hot.pop(0))
        if len(self.warm) > 20:
            self.cold.append(self.warm.pop(0))