from typing import Dict, Any

def apply_network(decision: Dict[str, Any]) -> Dict[str, Any]:
    """네트워크 슬라이스 API 호출 시뮬레이션"""
    return {
        "method": "POST",
        "path": "/api/v1/network/slice",
        "body": {
            "slice_type": decision.get("slice"),
            "qos_class": decision.get("qos_class")
        },
        "response": {"status": "applied", "slice_id": "slice-123"}
    }

def apply_ris(decision: Dict[str, Any]) -> Dict[str, Any]:
    """RIS API 호출 시뮬레이션"""
    return {
        "method": "PUT",
        "path": "/api/v1/ris/mode",
        "body": {
            "mode": decision.get("ris_mode")
        },
        "response": {"status": "configured", "ris_id": "ris-456"}
    }

def apply_ai_ran(decision: Dict[str, Any]) -> Dict[str, Any]:
    """AI-RAN API 호출 시뮬레이션"""
    return {
        "method": "PATCH",
        "path": "/api/v1/ai-ran/config",
        "body": decision.get("ai_ran_config", {}),
        "response": {"status": "updated", "config_version": "v2.1"}
    }