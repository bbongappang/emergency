import random
from datetime import datetime
from src.schema import RawInput

def generate_emergency_call():
    """응급통화/트리아지 텍스트 이벤트"""
    scenarios = [
        "65세 남성, 가슴 통증 호소, 호흡곤란 동반",
        "42세 여성, 교통사고 부상, 의식 명료",
        "3세 아동, 고열 39.2도, 경련 의심",
        "58세 남성, 뇌졸중 의심 증상, 편측 마비"
    ]
    return RawInput(
        source="emergency_call",
        type="triage_text",
        timestamp=datetime.now().isoformat(),
        payload={"text": random.choice(scenarios)}
    )

def generate_wearable_event():
    """웨어러블 생체신호 요약 이벤트"""
    hr = random.randint(45, 180)
    spo2 = random.randint(85, 100)
    alert = hr > 120 or spo2 < 92
    return RawInput(
        source="wearable_device",
        type="vital_summary",
        timestamp=datetime.now().isoformat(),
        payload={
            "heart_rate": hr,
            "spo2": spo2,
            "alert_triggered": alert
        }
    )

def generate_ecg_alarm():
    """심전도 알람/특징치 이벤트"""
    abnormal = random.choice([True, False, False])
    return RawInput(
        source="ecg_monitor",
        type="ecg_feature",
        timestamp=datetime.now().isoformat(),
        payload={
            "qt_interval": random.randint(350, 480),
            "st_deviation": round(random.uniform(-0.5, 2.0), 2),
            "abnormal_detected": abnormal
        }
    )

def generate_ambulance_event():
    """구급차 이동/모빌리티 이벤트"""
    eta = random.randint(3, 25)
    urgency = "high" if eta <= 8 else "medium"
    return RawInput(
        source="ambulance_fleet",
        type="mobility_status",
        timestamp=datetime.now().isoformat(),
        payload={
            "vehicle_id": f"AMB-{random.randint(100, 999)}",
            "eta_minutes": eta,
            "urgency_level": urgency,
            "location": f"서울시 {random.choice(['강남', '마포', '송파', '용산'])}구"
        }
    )

def generate_facility_congestion():
    """병동/응급실 혼잡도 운영 이벤트"""
    occupancy = random.randint(60, 105)
    return RawInput(
        source="hospital_operations",
        type="facility_congestion",
        timestamp=datetime.now().isoformat(),
        payload={
            "department": random.choice(["응급실", "중환자실", "일반병동"]),
            "occupancy_rate": occupancy,
            "waiting_count": random.randint(0, 45)
        }
    )

def generate_imaging_request():
    """영상 필요 요청 이벤트"""
    modality = random.choice(["CT", "MRI", "X-ray", "초음파"])
    priority = random.choice(["stat", "urgent", "routine"])
    return RawInput(
        source="imaging_system",
        type="imaging_request",
        timestamp=datetime.now().isoformat(),
        payload={
            "modality": modality,
            "priority": priority,
            "estimated_size_mb": random.randint(50, 500)
        }
    )

GENERATORS = {
    "응급통화/트리아지": generate_emergency_call,
    "웨어러블 생체신호": generate_wearable_event,
    "심전도 알람": generate_ecg_alarm,
    "구급차 이동": generate_ambulance_event,
    "병동 혼잡도": generate_facility_congestion,
    "영상 전송 요청": generate_imaging_request
}