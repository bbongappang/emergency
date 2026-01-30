from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class RawInput:
    source: str
    type: str
    timestamp: str
    payload: Dict[str, Any]

@dataclass
class StandardEvent:
    source: str
    type: str
    timestamp: str
    payload: Dict[str, Any]