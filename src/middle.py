from src.schema import StandardEvent
from src.front import FrontHierMemory
from typing import Dict, Any
import random

def make_intent(event: StandardEvent, memory: FrontHierMemory) -> Dict[str, Any]:
    """이벤트로부터 의도 추출"""
    intent_map = {
        "triage_text": "emergency_response",
        "vital_summary": "patient_monitoring",
        "ecg_feature": "cardiac_alert",
        "mobility_status": "ambulance_coordination",
        "facility_congestion": "resource_optimization",
        "imaging_request": "diagnostic_support"
    }
    
    return {
        "intent": intent_map.get(event.type, "unknown"),
        "priority": "high" if "emergency" in event.source or event.payload.get("alert_triggered") else "medium",
        "context_size": len(memory.hot) + len(memory.warm)
    }

def ml_generate_constraints(intent: Dict[str, Any]) -> Dict[str, Any]:
    """ML 기반 제약조건 생성 (시뮬레이션)"""
    priority = intent.get("priority", "medium")
    
    if priority == "high":
        return {
            "max_latency_ms": 30,
            "min_reliability": 0.9999,
            "bandwidth_mbps": 100,
            "penalty_weight": 10.0
        }
    else:
        return {
            "max_latency_ms": 100,
            "min_reliability": 0.99,
            "bandwidth_mbps": 50,
            "penalty_weight": 5.0
        }