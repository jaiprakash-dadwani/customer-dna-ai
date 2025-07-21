"""
Configuration settings for Customer DNA AI
"""

# Risk level thresholds
RISK_LEVELS = {
    'LOW': 30,
    'MEDIUM': 50,
    'HIGH': 70,
    'CRITICAL': 85
}

# Risk factor thresholds
RISK_THRESHOLDS = {
    'DEPOSIT_LOW': 10,
    'DEPOSIT_MEDIUM': 15,
    'DEPOSIT_HIGH': 20,
    'SPENDING_LOW': 10,
    'SPENDING_MEDIUM': 15,
    'SPENDING_HIGH': 20,
    'SESSION_LOW': 8,
    'SESSION_MEDIUM': 12,
    'SESSION_HIGH': 16,
    'LOCATION_LOW': 8,
    'LOCATION_HIGH': 12,
    'SUPPORT_LOW': 8,
    'SUPPORT_MEDIUM': 12,
    'SUPPORT_HIGH': 15
}

# Validation limits
VALIDATION_LIMITS = {
    'MAX_DEPOSIT': 50000,
    'MAX_WAGER': 10000,
    'MAX_SESSION_TIME': 720,
    'MAX_SUPPORT_CALLS': 20,
    'MAX_LOCATION_HISTORY': 50
}

# Profile multipliers for risk calculation
PROFILE_MULTIPLIERS = {
    'Low': {
        'deposit': 0.8,
        'spending': 0.8,
        'overall': 0.9
    },
    'Medium': {
        'deposit': 1.0,
        'spending': 1.0,
        'overall': 1.0
    },
    'High': {
        'deposit': 1.2,
        'spending': 1.2,
        'overall': 1.1
    },
    'Critical': {
        'deposit': 1.5,
        'spending': 1.5,
        'overall': 1.3
    }
}
