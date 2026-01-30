from typing import Dict, Any
import random

def decide(intent: Dict[str, Any], constraints: Dict[str, Any]) -> Dict[str, Any]:
    """최종 결정 수행 (규칙 기반)"""
    intent_type = intent.get("intent", "unknown")
    max_latency = constraints.get("max_latency_ms", 100)
    
    # 슬라이스 결정
    slice_map = {
        "emergency_response": "URLLC",
        "cardiac_alert": "URLLC",
        "ambulance_coordination": "URLLC",
        "patient_monitoring": "eMBB",
        "diagnostic_support": "eMBB",
        "resource_optimization": "mMTC"
    }
    
    slice_type = slice_map.get(intent_type, "eMBB")
    
    # RIS 모드 결정
    ris_mode = "intelligent" if max_latency < 50 else "default"
    
    # AI-RAN 설정
    ai_ran_config = {
        "beam_mode": "adaptive" if slice_type == "URLLC" else "standard",
        "power_level": "high" if slice_type == "URLLC" else "medium"
    }
    
    return {
        "slice": slice_type,
        "ris_mode": ris_mode,
        "ai_ran_config": ai_ran_config,
        "target_latency": max_latency,
        "qos_class": 1 if slice_type == "URLLC" else 5
    }