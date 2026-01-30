import streamlit as st
import json
from datetime import datetime
from src.generators import GENERATORS
from src.front import normalize, FrontHierMemory
from src.middle import make_intent, ml_generate_constraints
from src.optimizer import decide
from src.back import execute
from src.metrics import koi_from, effect_mapping

def init_session_state():
    if "memory" not in st.session_state:
        st.session_state.memory = FrontHierMemory()
    if "raw_input" not in st.session_state:
        st.session_state.raw_input = None
    if "standard_event" not in st.session_state:
        st.session_state.standard_event = None
    if "intent" not in st.session_state:
        st.session_state.intent = None
    if "constraints" not in st.session_state:
        st.session_state.constraints = None
    if "decision" not in st.session_state:
        st.session_state.decision = None
    if "api_calls" not in st.session_state:
        st.session_state.api_calls = []
    if "kpi_history" not in st.session_state:
        st.session_state.kpi_history = []
    if "koi_history" not in st.session_state:
        st.session_state.koi_history = []
    if "current_kpi" not in st.session_state:
        st.session_state.current_kpi = {}
    if "current_koi" not in st.session_state:
        st.session_state.current_koi = {}
    if "effects" not in st.session_state:
        st.session_state.effects = []

def render_status_bar():
    cols = st.columns(5)
    decision = st.session_state.decision or {}
    koi = st.session_state.current_koi or {}
    
    with cols[0]:
        stage = "대기 중"
        if st.session_state.decision:
            stage = "실행 완료"
        elif st.session_state.intent:
            stage = "처리 중"
        st.metric("현재 단계", stage)
    
    with cols[1]:
        slice_type = decision.get("slice", "없음")
        st.metric("슬라이스", slice_type)
    
    with cols[2]:
        ris = decision.get("ris_mode", "기본")
        st.metric("RIS 모드", ris)
    
    with cols[3]:
        ai_ran = decision.get("ai_ran_config", {}).get("beam_mode", "표준")
        st.metric("AI-RAN", ai_ran)
    
    with cols[4]:
        koi_score = koi.get("운영목표달성도", 0.0)
        st.metric("KOI 점수", f"{koi_score:.2f}")

def run_pipeline(generator_name):
    """전체 F-M-B 파이프라인 실행"""
    # Front
    raw = GENERATORS[generator_name]()
    st.session_state.raw_input = raw
    
    std_event = normalize(raw)
    st.session_state.standard_event = std_event
    st.session_state.memory.add(std_event)
    
    # Middle
    intent = make_intent(std_event, st.session_state.memory)
    st.session_state.intent = intent
    
    constraints = ml_generate_constraints(intent)
    st.session_state.constraints = constraints
    
    # Optimizer
    decision = decide(intent, constraints)
    st.session_state.decision = decision
    
    # Back
    api_calls = execute(decision)
    st.session_state.api_calls = api_calls
    
    # Metrics
    kpi = {
        "latency_ms": decision.get("target_latency", 50),
        "loss_rate": 0.001,
        "jitter_ms": 2.5,
        "coverage": 0.98
    }
    st.session_state.current_kpi = kpi
    st.session_state.kpi_history.append(kpi)
    if len(st.session_state.kpi_history) > 10:
        st.session_state.kpi_history.pop(0)
    
    koi = koi_from(kpi, decision)
    st.session_state.current_koi = koi
    st.session_state.koi_history.append(koi)
    if len(st.session_state.koi_history) > 10:
        st.session_state.koi_history.pop(0)
    
    effects = effect_mapping(decision, kpi, koi)
    st.session_state.effects = effects

def render_tab_collection():
    st.subheader("실시간 데이터 수집")
    
    cols = st.columns(6)
    for idx, name in enumerate(GENERATORS.keys()):
        with cols[idx]:
            if st.button(name, key=f"btn_{name}", use_container_width=True):
                run_pipeline(name)
    
    st.divider()
    
    cols = st.columns(3)
    with cols[0]:
        st.markdown("**입력 원문**")
        if st.session_state.raw_input:
            st.json(st.session_state.raw_input.__dict__, expanded=False)
    
    with cols[1]:
        st.markdown("**표준 이벤트**")
        if st.session_state.standard_event:
            st.json(st.session_state.standard_event.__dict__, expanded=False)
    
    with cols[2]:
        st.markdown("**이벤트 버스 출력**")
        if st.session_state.intent:
            st.json(st.session_state.intent, expanded=False)
    
    st.divider()
    st.markdown("**Front 계층형 메모리**")
    mem_cols = st.columns(3)
    with mem_cols[0]:
        st.caption("🔥 Hot (최근 5개)")
        st.json([e.__dict__ for e in st.session_state.memory.hot], expanded=False)
    with mem_cols[1]:
        st.caption("🌡️ Warm (최근 20개)")
        st.json([e.__dict__ for e in st.session_state.memory.warm], expanded=False)
    with mem_cols[2]:
        st.caption("❄️ Cold (전체)")
        st.caption(f"총 {len(st.session_state.memory.cold)}개 이벤트")

def render_tab_pipeline():
    st.subheader("F–M–B 파이프라인")
    
    cols = st.columns(4)
    
    with cols[0]:
        st.markdown("### Front")
        st.caption("입력 정규화 / 임베딩 / 메모리")
        if st.session_state.standard_event:
            st.json({
                "이벤트유형": st.session_state.standard_event.type,
                "출처": st.session_state.standard_event.source,
                "시간": st.session_state.standard_event.timestamp
            })
    
    with cols[1]:
        st.markdown("### Middle")
        st.caption("의도 파악 / 제약 생성")
        if st.session_state.intent:
            st.json({"의도": st.session_state.intent}, expanded=False)
        if st.session_state.constraints:
            st.json({"제약조건": st.session_state.constraints}, expanded=False)
    
    with cols[2]:
        st.markdown("### Optimizer")
        st.caption("규칙 기반 최종 결정")
        if st.session_state.decision:
            st.json(st.session_state.decision, expanded=False)
    
    with cols[3]:
        st.markdown("### Back")
        st.caption("API 실행 / 텔레메트리")
        if st.session_state.api_calls:
            st.caption(f"실행된 API: {len(st.session_state.api_calls)}개")
            for call in st.session_state.api_calls[:3]:
                st.text(f"{call['method']} {call['path']}")

def render_tab_api():
    st.subheader("API 콘솔")
    
    if st.session_state.decision:
        st.markdown("**Optimizer 결정 페이로드**")
        st.json(st.session_state.decision, expanded=True)
    
    st.divider()
    st.markdown("**API 호출 목록**")
    
    if st.session_state.api_calls:
        for idx, call in enumerate(st.session_state.api_calls):
            with st.expander(f"{idx+1}. {call['method']} {call['path']}"):
                st.json({
                    "요청 본문": call.get("body", {}),
                    "응답": call.get("response", {})
                })
    else:
        st.info("API 호출 기록이 없습니다.")

def render_tab_results():
    st.subheader("결과 및 효과")
    
    # KPI 테이블
    st.markdown("**KPI (Key Performance Indicators)**")
    if st.session_state.current_kpi:
        kpi = st.session_state.current_kpi
        kpi_cols = st.columns(4)
        with kpi_cols[0]:
            st.metric("지연시간", f"{kpi.get('latency_ms', 0)} ms")
        with kpi_cols[1]:
            st.metric("손실률", f"{kpi.get('loss_rate', 0):.3%}")
        with kpi_cols[2]:
            st.metric("지터", f"{kpi.get('jitter_ms', 0)} ms")
        with kpi_cols[3]:
            st.metric("커버리지", f"{kpi.get('coverage', 0):.1%}")
    
    st.divider()
    
    # KOI 메트릭
    st.markdown("**KOI (Key Outcome Indicators)**")
    if st.session_state.current_koi:
        koi = st.session_state.current_koi
        koi_cols = st.columns(3)
        with koi_cols[0]:
            st.metric("운영목표달성도", f"{koi.get('운영목표달성도', 0):.2f}")
        with koi_cols[1]:
            st.metric("비용효율성", f"{koi.get('비용효율성', 0):.2f}")
        with koi_cols[2]:
            st.metric("안정성지수", f"{koi.get('안정성지수', 0):.2f}")
    
    st.divider()
    
    # 추세 그래프
    if len(st.session_state.kpi_history) > 1:
        st.markdown("**최근 추세 (최대 10회)**")
        chart_cols = st.columns(2)
        
        with chart_cols[0]:
            st.line_chart([k.get('latency_ms', 0) for k in st.session_state.kpi_history])
            st.caption("KPI: 지연시간 추이")
        
        with chart_cols[1]:
            st.line_chart([k.get('운영목표달성도', 0) for k in st.session_state.koi_history])
            st.caption("KOI: 운영목표달성도 추이")
    
    st.divider()
    
    # 운영 효과 카드
    st.markdown("**운영 효과 (Effect Mapping)**")
    if st.session_state.effects:
        effect_cols = st.columns(3)
        for idx, eff in enumerate(st.session_state.effects[:3]):
            with effect_cols[idx]:
                st.info(f"**{eff['title']}**\n\n{eff['description']}")
    
    st.divider()
    
    # 발표용 요약
    if st.session_state.decision:
        slice_type = st.session_state.decision.get("slice", "기본")
        koi_score = st.session_state.current_koi.get("운영목표달성도", 0)
        summary = f"슬라이스 '{slice_type}' 적용 결과, 운영목표 달성도 {koi_score:.2f} 기록 — 통신을 운영 대상으로 관리하여 의료 서비스 품질을 향상시켰습니다."
        st.success(summary)

def render_ui():
    init_session_state()
    
    st.title("🏥 Agentic Network Operations 데모")
    st.caption("통신을 연결이 아닌 운영 대상으로 다루는 F–M–B 아키텍처")
    
    render_status_bar()
    st.divider()
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "1️⃣ 실시간 데이터 수집",
        "2️⃣ F–M–B 파이프라인",
        "3️⃣ API 콘솔",
        "4️⃣ 결과 및 효과"
    ])
    
    with tab1:
        render_tab_collection()
    
    with tab2:
        render_tab_pipeline()
    
    with tab3:
        render_tab_api()
    
    with tab4:
        render_tab_results()