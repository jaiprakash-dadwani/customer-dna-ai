"""
Utility functions for improved session management
"""
import streamlit as st
from config import VALIDATION_LIMITS

def safe_rerun():
    """Safe rerun with session state validation"""
    if 'session_data' in st.session_state and st.session_state.session_data is not None:
        st.rerun()
    else:
        st.error("Session data corrupted. Please refresh the page.")

def validate_input(input_type, value):
    """Validate user inputs against limits"""
    limits = {
        'deposit': VALIDATION_LIMITS['MAX_DEPOSIT'],
        'wager': VALIDATION_LIMITS['MAX_WAGER'],
        'session': VALIDATION_LIMITS['MAX_SESSION_TIME'],
        'support': VALIDATION_LIMITS['MAX_SUPPORT_CALLS']
    }
    
    max_value = limits.get(input_type, float('inf'))
    
    if value > max_value:
        return False, f"Maximum {input_type} limit is {max_value:,}"
    elif value < 0:
        return False, f"{input_type.title()} must be positive"
    else:
        return True, "Valid input"

def limit_location_history(location_history, max_items=50):
    """Limit location history to prevent memory issues"""
    if len(location_history) > max_items:
        return location_history[-max_items:]
    return location_history