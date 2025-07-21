"""
Final Demo Test - 3 Core Profiles
"""
from fixed_ml_system import fixed_ml

# Test profiles
profiles = {
    "Teacher": {
        "age": 34, "income": 28000, "profession": "Teacher", "risk_category": "High",
        "monthly_limit": 500, "avg_session": 180, "work_stress": "High",
        "support_contacts": 6, "financial_stress": 8
    },
    "Executive": {
        "age": 42, "income": 65000, "profession": "Executive", "risk_category": "Medium",
        "monthly_limit": 1200, "avg_session": 120, "work_stress": "Medium",
        "support_contacts": 2, "financial_stress": 4
    },
    "Business Owner": {
        "age": 29, "income": 42000, "profession": "Business Owner", "risk_category": "Critical",
        "monthly_limit": 2000, "avg_session": 300, "work_stress": "Very High",
        "support_contacts": 12, "financial_stress": 10
    }
}

print("=== DEMO TEST: 3 Core Profiles ===")

for name, profile in profiles.items():
    print(f"\n{name.upper()}:")
    
    # Low activity scenario
    session_low = {
        'balance': 100, 'wagered': 50, 'session_time': profile['avg_session'],
        'location': 'Home', 'support_calls': 0,
        'deposits': [100], 'wagers': [50], 'location_history': []
    }
    
    result_low = fixed_ml.predict_risk(profile, session_low)
    print(f"  Low Activity: {result_low['risk_score']}% ({result_low['method']})")
    
    # High activity scenario
    session_high = {
        'balance': 200, 'wagered': 600, 'session_time': profile['avg_session'] * 2,
        'location': 'Casino', 'support_calls': 2,
        'deposits': [400, 300], 'wagers': [300, 300], 'location_history': ['Casino']
    }
    
    result_high = fixed_ml.predict_risk(profile, session_high)
    print(f"  High Activity: {result_high['risk_score']}% ({result_high['method']})")

print(f"\nML Training Samples: {fixed_ml.training_data.__len__()}")
print("=== READY FOR DEMO ===")