from typing import Dict, Any, List
import random

def koi_from(kpi: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    """KPI에서 KOI 계산"""
    latency = kpi.get("latency_ms", 50)
    loss = kpi.get("loss_rate", 0.001)
    coverage = kpi.get("coverage", 0.98)
    
    # 운영목표달성도: 지연·손실·커버리지 종합
    goal_score = (1 - latency/100) * 0.4 + (1 - loss) * 0.3 + coverage * 0.3
    
    # 비용효율성: 슬라이스 타입에 따라
    cost_eff = 0.9 if decision.get("slice") == "URLLC" else 0.7
    
    # 안정성지수
    stability = coverage * (1 - loss)
    
    return {
        "운영목표달성도": round(goal_score, 3),
        "비용효율성": round(cost_eff, 3),
        "안정성지수": round(stability, 3)
    }

def effect_mapping(decision: Dict[str, Any], kpi: Dict[str, Any], koi: Dict[str, Any]) -> List[Dict[str, Any]]:
    """운영 효과 설명 생성"""
    slice_type = decision.get("slice", "eMBB")
    ris_mode = decision.get("ris_mode", "default")
    
    effects = [
        {
            "title": f"슬라이스 {slice_type} 적용",
            "description": f"목표 지연시간 {decision.get('target_latency')}ms 달성을 위한 전용 슬라이스 할당"
        },
        {
            "title": f"RIS {ris_mode} 모드",
            "description": "재구성 가능 지능형 표면으로 커버리지 향상 및 간섭 최소화"
        },
        {
            "title": "AI-RAN 최적화",
            "description": f"빔포밍 모드 {decision.get('ai_ran_config', {}).get('beam_mode', 'standard')}로 스펙트럼 효율 극대화"
        }
    ]
    
    return effects
