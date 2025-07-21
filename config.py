"""
Configuration constants - Externalized magic numbers
"""

# Risk Calculation Thresholds
RISK_THRESHOLDS = {
    'DEPOSIT_LOW': 8,
    'DEPOSIT_MEDIUM': 15,
    'DEPOSIT_HIGH': 22,
    'SPENDING_LOW': 8,
    'SPENDING_MEDIUM': 15,
    'SPENDING_HIGH': 22,
    'SESSION_LOW': 10,
    'SESSION_MEDIUM': 15,
    'SESSION_HIGH': 18,
    'LOCATION_LOW': 10,
    'LOCATION_HIGH': 15,
    'SUPPORT_LOW': 8,
    'SUPPORT_MEDIUM': 12,
    'SUPPORT_HIGH': 15
}

# Risk Level Boundaries
RISK_LEVELS = {
    'CRITICAL': 80,
    'HIGH': 60,
    'MEDIUM': 40,
    'LOW': 0
}

# Input Validation Limits
VALIDATION_LIMITS = {
    'MAX_DEPOSIT': 50000,
    'MAX_WAGER': 25000,
    'MAX_SESSION_TIME': 1440,
    'MAX_SUPPORT_CALLS': 20
}

# Profile Multipliers
PROFILE_MULTIPLIERS = {
    'Critical': {'deposit': 1.4, 'spending': 1.3, 'support': 1.2, 'overall': 1.2},
    'High': {'deposit': 1.2, 'spending': 1.1, 'support': 1.0, 'overall': 1.1},
    'Medium': {'deposit': 1.0, 'spending': 1.0, 'support': 1.0, 'overall': 1.0}
}