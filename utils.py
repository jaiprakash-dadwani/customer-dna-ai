"""
Utility functions for Customer DNA AI
"""
import streamlit as st
import time

def safe_rerun():
    """Safe rerun with delay to prevent rapid refreshes"""
    time.sleep(0.1)
    st.rerun()

def validate_input(value, min_val=0, max_val=float('inf')):
    """Validate numeric input within bounds"""
    try:
        num_val = float(value)
        return min_val <= num_val <= max_val
    except (ValueError, TypeError):
        return False

def limit_location_history(history, max_items=50):
    """Limit location history to prevent memory issues"""
    if len(history) > max_items:
        return history[-max_items:]
    return history
