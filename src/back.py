from typing import Dict, Any, List
from src.api_sim import apply_network, apply_ris, apply_ai_ran

def execute(decision: Dict[str, Any]) -> List[Dict[str, Any]]:
    """결정을 API 호출로 실행"""
    api_calls = []
    
    # 네트워크 슬라이스 적용
    net_call = apply_network(decision)
    api_calls.append(net_call)
    
    # RIS 적용
    if decision.get("ris_mode") != "default":
        ris_call = apply_ris(decision)
        api_calls.append(ris_call)
    
    # AI-RAN 적용
    ai_ran_call = apply_ai_ran(decision)
    api_calls.append(ai_ran_call)
    
    return api_calls