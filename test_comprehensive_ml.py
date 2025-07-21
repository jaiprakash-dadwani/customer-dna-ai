"""
Test comprehensive ML system with interconnected features
"""
from fixed_ml_system import fixed_ml

print("=== TESTING COMPREHENSIVE ML SYSTEM ===")

# Test Executive profile
profile = {
    "age": 42, "income": 65000, "profession": "Executive", "risk_category": "Medium",
    "monthly_limit": 1200, "avg_session": 120, "work_stress": "Medium",
    "support_contacts": 2, "financial_stress": 4
}

# Test 1: Small deposit, no wagering (should be very low risk)
session1 = {
    'balance': 100, 'wagered': 0, 'session_time': 60,
    'location': 'Home', 'support_calls': 0,
    'deposits': [100], 'wagers': [], 'location_history': []
}

result1 = fixed_ml.predict_risk(profile, session1)
print(f"Small deposit, no wager: {result1['risk_score']}% - Should be LOW (15-25%)")

# Test 2: Moderate deposit + small wager (should be low-medium)
session2 = {
    'balance': 200, 'wagered': 100, 'session_time': 120,
    'location': 'Home', 'support_calls': 0,
    'deposits': [300], 'wagers': [100], 'location_history': []
}

result2 = fixed_ml.predict_risk(profile, session2)
print(f"Moderate activity: {result2['risk_score']}% - Should be LOW-MEDIUM (25-40%)")

# Test 3: Large deposit + high wagering + casino (multiple risk factors)
session3 = {
    'balance': 100, 'wagered': 800, 'session_time': 300,
    'location': 'Casino', 'support_calls': 2,
    'deposits': [500, 400], 'wagers': [400, 400], 'location_history': ['Casino', 'Casino']
}

result3 = fixed_ml.predict_risk(profile, session3)
print(f"High risk combination: {result3['risk_score']}% - Should be HIGH (60-80%)")

# Test 4: Teacher profile (higher baseline risk)
teacher_profile = {
    "age": 34, "income": 28000, "profession": "Teacher", "risk_category": "High",
    "monthly_limit": 500, "avg_session": 180, "work_stress": "High",
    "support_contacts": 6, "financial_stress": 8
}

session4 = {
    'balance': 50, 'wagered': 200, 'session_time': 240,
    'location': 'Work', 'support_calls': 1,
    'deposits': [250], 'wagers': [200], 'location_history': ['Work']
}

result4 = fixed_ml.predict_risk(teacher_profile, session4)
print(f"Teacher high stress: {result4['risk_score']}% - Should be HIGH (65-85%)")

print(f"\nML Features: {len(fixed_ml.feature_names)}")
print(f"Training samples: {len(fixed_ml.training_data)}")
print("=== COMPREHENSIVE ML TEST COMPLETE ===")