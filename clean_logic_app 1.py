"""
Customer DNA AI - Clean Logic Implementation
Rebuilt from scratch with working logic
"""
import streamlit as st
import pandas as pd
import time
from datetime import datetime
from config import RISK_THRESHOLDS, RISK_LEVELS, VALIDATION_LIMITS, PROFILE_MULTIPLIERS
from utils import safe_rerun, validate_input, limit_location_history

st.set_page_config(page_title="Customer DNA AI - Clean Logic", page_icon="🧬", layout="wide")

# Customer Profiles
CUSTOMERS = {
    "Sarah Martinez - Teacher": {
        "age": 34, "income": 28000, "risk_category": "High",
        "current_balance": 245, "monthly_limit": 800, "avg_session": 280,
        "support_contacts": 8, "financial_stress": 8, "emotional_state": "Distressed"
    },
    "Michael Thompson - Executive": {
        "age": 42, "income": 65000, "risk_category": "Medium", 
        "current_balance": 1250, "monthly_limit": 2000, "avg_session": 120,
        "support_contacts": 2, "financial_stress": 4, "emotional_state": "Stable"
    },
    "David Chen - Business Owner": {
        "age": 29, "income": 42000, "risk_category": "Critical",
        "current_balance": 85, "monthly_limit": 5000, "avg_session": 420,
        "support_contacts": 12, "financial_stress": 10, "emotional_state": "Crisis"
    }
}

def calculate_risk(profile, session_data):
    """Enhanced risk calculation with learning ML system"""
    try:
        # Use fixed ML system that learns from data
        from fixed_ml_system import fixed_ml
        
        # Get ML prediction (pure ML, no hardcoded rules)
        ml_prediction = fixed_ml.predict_risk(profile, session_data)
        
        # Add this interaction to training data for continuous learning
        fixed_ml.add_training_sample(profile, session_data)
        
        ml_risk_score = ml_prediction['risk_score']
        ml_confidence = ml_prediction['confidence']
        ml_method = ml_prediction['method']
        ml_samples = ml_prediction.get('samples_used', 0)
        
    except Exception as e:
        print(f"ML Error: {e}")
        # Pure rule-based fallback
        ml_risk_score = 50  # Default
        ml_confidence = 0.5
        ml_method = 'error_fallback'
        ml_samples = 0
    

    
    # Always calculate rule-based factors for comparison and display
    deposits = session_data.get('deposits', [])
    wagers = session_data.get('wagers', [])
    monthly_income = profile['income'] / 12
    
    # Rule-based calculation for factors
    factors = {}
    rule_risk_score = 0
    
    # Deposit Risk (0-25)
    if deposits:
        deposit_ratio = sum(deposits) / monthly_income if monthly_income > 0 else 0
        if deposit_ratio > 2.0:
            deposit_factor = 25
        elif deposit_ratio > 1.0:
            deposit_factor = 18
        elif deposit_ratio > 0.5:
            deposit_factor = 12
        else:
            deposit_factor = 5
        deposit_factor += min(5, len(deposits))
    else:
        deposit_factor = 0
    factors['Deposit'] = min(25, deposit_factor)
    rule_risk_score += factors['Deposit']
    
    # Spending Risk (0-25)
    if session_data['wagered'] > 0:
        spend_ratio = session_data['wagered'] / monthly_income if monthly_income > 0 else 0
        if spend_ratio > 1.5:
            spend_factor = 25
        elif spend_ratio > 1.0:
            spend_factor = 20
        elif spend_ratio > 0.5:
            spend_factor = 15
        else:
            spend_factor = 8
        spend_factor += min(5, len(wagers))
    else:
        spend_factor = 0
    factors['Spending'] = min(25, spend_factor)
    rule_risk_score += factors['Spending']
    
    # Session Risk (0-20)
    session_ratio = session_data['session_time'] / profile['avg_session'] if profile['avg_session'] > 0 else 1
    if session_ratio > 2.0:
        session_factor = 20
    elif session_ratio > 1.5:
        session_factor = 15
    else:
        session_factor = 8
    factors['Session'] = session_factor
    rule_risk_score += session_factor
    
    # Location Risk (0-15)
    location = session_data['location']
    if location in ['Casino', 'Betting Shop']:
        location_factor = 15
    elif location == 'Work':
        location_factor = 10
    else:
        location_factor = 5
    factors['Location'] = location_factor
    rule_risk_score += location_factor
    
    # Support Risk (0-15)
    total_support = profile['support_contacts'] + session_data['support_calls']
    if total_support > 10:
        support_factor = 15
    elif total_support > 5:
        support_factor = 12
    else:
        support_factor = 6
    support_factor += profile['financial_stress']
    factors['Support'] = min(15, support_factor)
    rule_risk_score += factors['Support']
    
    # Apply profile multiplier
    multiplier = PROFILE_MULTIPLIERS.get(profile['risk_category'], PROFILE_MULTIPLIERS['Medium'])
    rule_risk_score *= multiplier['overall']
    rule_risk_score = min(100, int(rule_risk_score))
    
    # Use ML score if available and confident, otherwise use rule-based
    if ml_method == 'ml_prediction' and ml_confidence > 0.7:
        final_score = ml_risk_score
        # Scale factors to match ML score
        if rule_risk_score > 0:
            scale = final_score / rule_risk_score
            factors = {k: min(25 if k in ['Deposit', 'Spending'] else 20 if k == 'Session' else 15, 
                             int(v * scale)) for k, v in factors.items()}
    else:
        final_score = rule_risk_score
    
    # Determine risk level
    if final_score >= 80:
        risk_level = "CRITICAL"
    elif final_score >= 60:
        risk_level = "HIGH"
    elif final_score >= 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"
    
    return {
        'score': final_score,
        'level': risk_level,
        'factors': factors,
        'ml_used': ml_method == 'ml_prediction',
        'ml_confidence': ml_confidence,
        'ml_method': ml_method,
        'ml_samples': ml_samples,
        'rule_score': rule_risk_score,
        'learning_active': True
    }

def get_interventions(risk_result, profile):
    """Simple intervention logic"""
    interventions = []
    factors = risk_result['factors']
    
    if factors['Deposit'] >= RISK_THRESHOLDS['DEPOSIT_LOW']:
        if factors['Deposit'] >= RISK_THRESHOLDS['DEPOSIT_HIGH']:
            urgency = 'CRITICAL'
            action = 'Immediate deposit intervention - Multiple large deposits detected'
        elif factors['Deposit'] >= RISK_THRESHOLDS['DEPOSIT_MEDIUM']:
            urgency = 'HIGH'
            action = 'Deposit monitoring - Pattern of concern identified'
        else:
            urgency = 'MEDIUM'
            action = 'Deposit tracking - Early warning triggered'
        
        interventions.append({
            'type': 'Deposit Controls',
            'urgency': urgency,
            'action': action
        })
    
    if factors['Spending'] >= RISK_THRESHOLDS['SPENDING_LOW']:
        if factors['Spending'] >= RISK_THRESHOLDS['SPENDING_HIGH']:
            urgency = 'CRITICAL'
            action = 'Immediate spend intervention - Excessive wagering detected'
        elif factors['Spending'] >= RISK_THRESHOLDS['SPENDING_MEDIUM']:
            urgency = 'HIGH'
            action = 'Spend limits - Monthly limit breached or high frequency'
        else:
            urgency = 'MEDIUM'
            action = 'Spend monitoring - Escalating wagering pattern'
        
        interventions.append({
            'type': 'Spend Management', 
            'urgency': urgency,
            'action': action
        })
    
    if factors['Session'] >= RISK_THRESHOLDS['SESSION_LOW']:
        urgency = 'CRITICAL' if factors['Session'] >= RISK_THRESHOLDS['SESSION_HIGH'] else 'HIGH' if factors['Session'] >= RISK_THRESHOLDS['SESSION_MEDIUM'] else 'MEDIUM'
        interventions.append({
            'type': 'Session Management',
            'urgency': urgency, 
            'action': 'Time limits and break reminders'
        })
    
    if factors['Location'] >= RISK_THRESHOLDS['LOCATION_LOW']:
        urgency = 'HIGH' if factors['Location'] >= RISK_THRESHOLDS['LOCATION_HIGH'] else 'MEDIUM'
        interventions.append({
            'type': 'Location Monitoring',
            'urgency': urgency,
            'action': 'Venue alerts, GPS tracking, and safe zone reminders'
        })
    
    if factors['Support'] >= RISK_THRESHOLDS['SUPPORT_LOW']:
        if factors['Support'] >= RISK_THRESHOLDS['SUPPORT_HIGH']:
            urgency = 'CRITICAL'
            action = 'Immediate crisis intervention and counselor assignment'
        elif factors['Support'] >= RISK_THRESHOLDS['SUPPORT_MEDIUM']:
            urgency = 'HIGH'
            action = 'Priority counselor contact and support escalation'
        else:
            urgency = 'MEDIUM'
            action = 'Enhanced support monitoring and check-ins'
        
        interventions.append({
            'type': 'Enhanced Support',
            'urgency': urgency,
            'action': action
        })
    
    # Sort by urgency
    urgency_order = {'HIGH': 0, 'MEDIUM': 1}
    interventions.sort(key=lambda x: urgency_order.get(x['urgency'], 2))
    
    return interventions

def init_session():
    """Initialize session state - FIXED: Start with zero balance"""
    if 'session_data' not in st.session_state:
        first_customer = list(CUSTOMERS.keys())[0]
        first_profile = CUSTOMERS[first_customer]
        st.session_state.session_data = {
            'customer': first_customer,
            'balance': 0.0,  # Start with zero balance - must deposit to wager
            'wagered': 0,
            'session_time': first_profile['avg_session'],
            'location': 'Home',
            'support_calls': 0,
            'deposits': [],
            'wagers': [],
            'location_history': []
        }

def main():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Mulish:wght@400;600;700&display=swap');
    
    .main > div { padding-top: 0.5rem; font-family: 'Mulish', sans-serif; font-weight: 400; }
    .header { background: #8F00BF; color: white; padding: 2rem; border-radius: 15px; margin-bottom: 2rem; }
    .card { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 10px 25px rgba(143, 0, 191, 0.1); margin-bottom: 1.5rem; border: 1px solid rgba(143, 0, 191, 0.1); }
    .stat-card { background: #8F00BF; color: white; padding: 1.5rem; border-radius: 12px; text-align: center; }
    .risk-critical { background: #dc2626; box-shadow: 0 0 20px rgba(220, 38, 38, 0.5); }
    .risk-high { background: #f59e0b; box-shadow: 0 0 15px rgba(245, 158, 11, 0.4); }
    .nav-button { background: #8F00BF; color: white; padding: 0.5rem 1rem; border-radius: 8px; text-decoration: none; margin: 0 0.5rem; }
    
    h1, h2, h3, h4, h5, h6 { font-family: 'Mulish', sans-serif; font-weight: 600; color: #8F00BF; }
    p, div, span, li { font-family: 'Mulish', sans-serif; font-weight: 400; }
    .stButton > button { background-color: #8F00BF; color: white; border: none; font-family: 'Mulish', sans-serif; font-weight: 600; }
    .stButton > button:hover { background-color: #7A00A3; }
    .stSelectbox > div > div { font-family: 'Mulish', sans-serif; }
    .stNumberInput > div > div > input { font-family: 'Mulish', sans-serif; }
    </style>
    """, unsafe_allow_html=True)
    
    # Navigation
    col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 4])
    with col_nav1:
        if st.button("🏠 Main Dashboard", key="nav_main"):
            st.session_state.page = "main"
            st.rerun()
    with col_nav2:
        if st.button("🤖 AI Model Details", key="nav_ai"):
            st.session_state.page = "ai_model"
            st.rerun()
    
    # Page routing
    if 'page' not in st.session_state:
        st.session_state.page = "main"
    
    if st.session_state.page == "ai_model":
        from ai_clean_ui_page import show_ai_model_page
        show_ai_model_page()
        return
    
    init_session()
    
    # Check if session_data exists
    if 'session_data' not in st.session_state or st.session_state.session_data is None:
        st.error("Session data not initialized. Please refresh the page.")
        st.stop()
    
    # Header
    st.markdown("""
    <div class='header'>
        <div style='display: flex; align-items: center; gap: 1rem;'>
            <div style='font-size: 2.5rem;'>🧬</div>
            <div>
                <h1 style='margin: 0; font-size: 2rem; font-weight: 600; font-family: Mulish, sans-serif;'>Customer DNA AI - Clean Logic</h1>
                <p style='margin: 0.5rem 0 0 0; opacity: 0.9; font-family: Mulish, sans-serif; font-weight: 400;'>Real-time Risk Assessment & Intervention System</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Get current data with enhanced AI analysis
    profile = CUSTOMERS[st.session_state.session_data['customer']]
    
    # Add occupation to profile for AI model
    customer_name = st.session_state.session_data['customer']
    if 'Teacher' in customer_name:
        profile['occupation'] = 'Teacher'
    elif 'Executive' in customer_name:
        profile['occupation'] = 'Executive'
    elif 'Business Owner' in customer_name:
        profile['occupation'] = 'Business Owner'
    else:
        profile['occupation'] = 'Other'
    
    risk_result = calculate_risk(profile, st.session_state.session_data)
    
    # Stats Cards
    balance = st.session_state.session_data['balance']
    wagered = st.session_state.session_data['wagered']
    session_time = st.session_state.session_data['session_time']
    support_calls = st.session_state.session_data['support_calls']
    
    # Risk-based highlighting
    deposit_class = 'risk-critical' if risk_result['factors']['Deposit'] >= 20 else 'risk-high' if risk_result['factors']['Deposit'] >= 15 else ''
    spend_class = 'risk-critical' if risk_result['factors']['Spending'] >= 20 else 'risk-high' if risk_result['factors']['Spending'] >= 15 else ''
    session_class = 'risk-critical' if risk_result['factors']['Session'] >= 15 else 'risk-high' if risk_result['factors']['Session'] >= 10 else ''
    support_class = 'risk-critical' if risk_result['factors']['Support'] >= 15 else 'risk-high' if risk_result['factors']['Support'] >= 10 else ''
    
    st.markdown(f"""
    <div style='display: grid; grid-template-columns: repeat(5, 1fr); gap: 1rem; margin-bottom: 2rem;'>
        <div class='stat-card {deposit_class}'>
            <div style='font-size: 1.5rem; font-weight: 800;'>£{sum(st.session_state.session_data.get('deposits', [])):,.0f}</div>
            <div style='font-size: 0.8rem; opacity: 0.9;'>DEPOSITS</div>
        </div>
        <div class='stat-card {spend_class}'>
            <div style='font-size: 1.5rem; font-weight: 800;'>£{wagered:,.0f}</div>
            <div style='font-size: 0.8rem; opacity: 0.9;'>WAGERED</div>
        </div>
        <div class='stat-card {session_class}'>
            <div style='font-size: 1.5rem; font-weight: 800;'>{session_time}</div>
            <div style='font-size: 0.8rem; opacity: 0.9;'>SESSION</div>
        </div>
        <div class='stat-card {support_class}'>
            <div style='font-size: 1.5rem; font-weight: 800;'>{support_calls}</div>
            <div style='font-size: 0.8rem; opacity: 0.9;'>SUPPORT</div>
        </div>
        <div class='stat-card'>
            <div style='font-size: 1.5rem; font-weight: 800;'>{risk_result['score']}%</div>
            <div style='font-size: 0.8rem; opacity: 0.9;'>RISK</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Notifications
    if risk_result['level'] == 'CRITICAL':
        st.error(f"🚨 CRITICAL RISK ({risk_result['score']}%) - Immediate intervention required!")
    elif risk_result['level'] == 'HIGH':
        st.warning(f"⚠️ HIGH RISK ({risk_result['score']}%) - Close monitoring needed")
    elif risk_result['level'] == 'MEDIUM':
        st.info(f"ℹ️ MEDIUM RISK ({risk_result['score']}%) - Preventive measures recommended")
    
    # Three columns
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("<div class='card'><h3 style='font-family: Mulish, sans-serif; font-weight: 600; color: #8F00BF;'>👤 Customer Controls</h3>", unsafe_allow_html=True)
        
        # Customer selection
        selected = st.selectbox("Select Customer", list(CUSTOMERS.keys()), 
                               index=list(CUSTOMERS.keys()).index(st.session_state.session_data['customer']))
        
        if selected != st.session_state.session_data['customer']:
            # Reset data for new customer - FIXED: Start with zero balance
            new_profile = CUSTOMERS[selected]
            st.session_state.session_data = {
                'customer': selected,
                'balance': 0.0,  # Start with zero balance - must deposit to wager
                'wagered': 0,
                'session_time': new_profile['avg_session'],
                'location': 'Home',
                'support_calls': 0,
                'deposits': [],
                'wagers': [],
                'location_history': []
            }
            st.rerun()
        
        # Enhanced profile info with AI insights
        total_deposits = sum(st.session_state.session_data.get('deposits', []))
        deposit_count = len(st.session_state.session_data.get('deposits', []))
        total_wagers = sum(st.session_state.session_data.get('wagers', []))
        wager_count = len(st.session_state.session_data.get('wagers', []))
        monthly_income = profile['income'] / 12
        deposit_ratio = (total_deposits / monthly_income) if monthly_income > 0 else 0
        spend_ratio = (st.session_state.session_data['wagered'] / monthly_income) if monthly_income > 0 else 0
        
        # Enhanced ML Learning Insights
        ml_method = risk_result.get('ml_method', 'unknown')
        ml_samples = risk_result.get('ml_samples', 0)
        ai_confidence = risk_result['ml_confidence'] * 100
        crisis_probability = risk_result['score']
        days_to_crisis = max(1, 21 - int(crisis_probability * 0.2))
        
        # ML Status
        if ml_method == 'ml_prediction':
            ml_status = f"ML Learning ({ml_samples} samples)"
        elif ml_method == 'rule_based_fallback':
            ml_status = f"ML Fallback ({ml_samples} samples)"
        else:
            ml_status = "Rule-based (Learning)"
        
        st.markdown(f"""
        <div style='background: rgba(143, 0, 191, 0.05); padding: 1rem; border-radius: 8px; margin: 1rem 0; font-size: 0.8rem; border: 1px solid rgba(143, 0, 191, 0.2); font-family: Mulish, sans-serif;'>
            <div><strong style='color: #8F00BF;'>Profile:</strong> {profile['age']}y, £{profile['income']:,}/year, {profile['risk_category']} Risk</div>
            <div><strong style='color: #8F00BF;'>Limits:</strong> Monthly £{profile['monthly_limit']:,} | Current Balance: £{st.session_state.session_data['balance']:,.0f}</div>
            <div><strong style='color: #8F00BF;'>Deposits:</strong> {deposit_count} deposits = £{total_deposits:,.0f} ({deposit_ratio:.1f}x monthly income)</div>
            <div><strong style='color: #8F00BF;'>Wagers:</strong> {wager_count} wagers = £{st.session_state.session_data['wagered']:,.0f} ({spend_ratio:.1f}x monthly income)</div>
            <div><strong style='color: #8F00BF;'>Status:</strong> {profile['emotional_state']}, Stress: {profile['financial_stress']}/10, Support: {profile['support_contacts'] + st.session_state.session_data['support_calls']}</div>
            <div style='color: #8F00BF; font-weight: 600;'><strong>🤖 ML Analysis:</strong> {ml_status}</div>
            <div style='color: #8F00BF; font-weight: 400; font-size: 0.75rem;'>Confidence: {ai_confidence:.1f}% | Crisis: ~{days_to_crisis} days | Learning: Active</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add Deposit - MONITORING ONLY
        col_dep, col_btn1 = st.columns([3, 1])
        with col_dep:
            deposit_input = st.number_input("💰 Add Deposit", min_value=0.0, max_value=float(VALIDATION_LIMITS['MAX_DEPOSIT']), value=0.0, step=50.0, key="deposit_input")
        with col_btn1:
            if st.button("Add", key="add_deposit"):
                if deposit_input > 0:
                    st.session_state.session_data['balance'] += deposit_input
                    st.session_state.session_data['deposits'].append(deposit_input)
                    
                    # Enhanced monitoring alerts
                    monthly_income = profile['income'] / 12
                    total_deposits_now = sum(st.session_state.session_data['deposits'])
                    
                    if profile['risk_category'] == 'Critical' and deposit_input > monthly_income * 0.5:
                        st.error(f"🚨 CRITICAL ALERT: Large deposit £{deposit_input:,.0f} for high-risk customer")
                    elif profile['risk_category'] == 'High' and deposit_input > monthly_income * 0.7:
                        st.warning(f"⚠️ HIGH RISK ALERT: Large deposit £{deposit_input:,.0f}")
                    elif deposit_input > monthly_income:
                        st.warning(f"⚠️ MONITOR: Deposit £{deposit_input:,.0f} exceeds monthly income")
                    
                    # Total deposit monitoring
                    if total_deposits_now > monthly_income * 2:
                        st.error(f"🚨 ESCALATION: Total deposits £{total_deposits_now:,.0f} exceed 2x monthly income")
                    
                    st.success(f"✅ +£{deposit_input:,.0f}")
                    safe_rerun()
                else:
                    st.error("Enter amount > 0")
        
        # Place Wager - FIXED: Proper balance validation
        col_wag, col_btn2 = st.columns([3, 1])
        with col_wag:
            current_balance = float(st.session_state.session_data['balance'])
            if current_balance <= 0:
                st.number_input("🎯 Place Wager", min_value=0.0, max_value=0.0, value=0.0, disabled=True, key="wager_input", help="Add deposit first to place wagers")
            else:
                max_wager = float(min(current_balance, VALIDATION_LIMITS['MAX_WAGER']))
                wager_input = st.number_input("🎯 Place Wager", min_value=0.0, max_value=max_wager, value=0.0, step=25.0, key="wager_input")
        with col_btn2:
            if st.button("Place", key="place_wager"):
                current_balance = st.session_state.session_data['balance']
                if current_balance <= 0:
                    st.error("🚨 No balance available! Add deposit first.")
                elif 'wager_input' in st.session_state and st.session_state.wager_input > 0:
                    wager_amount = st.session_state.wager_input
                    if wager_amount <= current_balance:
                        st.session_state.session_data['balance'] -= wager_amount
                        st.session_state.session_data['wagered'] += wager_amount
                        st.session_state.session_data['wagers'].append(wager_amount)
                        
                        # Enhanced wager monitoring
                        monthly_income = profile['income'] / 12
                        monthly_limit = profile.get('monthly_limit', monthly_income)
                        new_total_wagered = st.session_state.session_data['wagered']
                        
                        if profile['risk_category'] == 'Critical' and wager_amount > monthly_income * 0.3:
                            st.error(f"🚨 CRITICAL ALERT: Large wager £{wager_amount:,.0f} for high-risk customer")
                        elif new_total_wagered > monthly_limit:
                            st.error(f"🚨 LIMIT BREACH: Total wagered £{new_total_wagered:,.0f} exceeds monthly limit £{monthly_limit:,.0f}")
                        elif wager_amount > monthly_income * 0.4:
                            st.warning(f"⚠️ MONITOR: Large wager £{wager_amount:,.0f}")
                        
                        # Frequency monitoring
                        wager_count = len(st.session_state.session_data['wagers'])
                        if wager_count > 8:
                            st.warning(f"⚠️ FREQUENCY ALERT: {wager_count} wagers placed")
                        
                        st.success(f"✅ Wagered £{wager_amount:,.0f}")
                        st.rerun()
                    else:
                        st.error(f"🚨 Insufficient balance! Available: £{current_balance:,.0f}")
                else:
                    st.error("Enter wager amount > 0")
        
        # Session Time
        col_sess, col_btn3 = st.columns([3, 1])
        with col_sess:
            session_input = st.number_input("⏱️ Session (min)", min_value=0, max_value=int(VALIDATION_LIMITS['MAX_SESSION_TIME']), value=int(st.session_state.session_data['session_time']), step=15, key="session_input")
        with col_btn3:
            if st.button("Set", key="set_session"):
                st.session_state.session_data['session_time'] = int(session_input)
                st.success(f"✅ {int(session_input)} min")
                st.rerun()
        
        # Location - Enhanced
        current_location = st.session_state.session_data['location']
        location_options = ["Home", "Work", "Casino", "Betting Shop", "Public"]
        location_index = location_options.index(current_location) if current_location in location_options else 0
        location = st.selectbox("📍 Location", location_options, index=location_index, key="location_select")
        
        if location != st.session_state.session_data['location']:
            # Track location history with limits
            if 'location_history' not in st.session_state.session_data:
                st.session_state.session_data['location_history'] = []
            st.session_state.session_data['location_history'].append(location)
            st.session_state.session_data['location_history'] = limit_location_history(
                st.session_state.session_data['location_history']
            )
            
            st.session_state.session_data['location'] = location
            
            # Location change warnings
            if location in ['Casino', 'Betting Shop']:
                if profile['risk_category'] == 'Critical':
                    st.error(f"🚨 CRITICAL: High-risk customer at {location}")
                else:
                    st.warning(f"⚠️ High-risk location: {location}")
            elif location == 'Work':
                st.info(f"🏢 Gambling at work detected")
            
            st.rerun()
        
        # Show location history
        location_history = st.session_state.session_data.get('location_history', [])
        if location_history:
            high_risk_count = sum(1 for loc in location_history if loc in ['Casino', 'Betting Shop'])
            if high_risk_count > 0:
                st.write(f"📍 Location History: {len(location_history)} visits, {high_risk_count} high-risk")
        
        # Contact Support - Enhanced
        col_supp, col_btn4 = st.columns([3, 1])
        with col_supp:
            st.write("📞 Support Contacts")
            total_support = profile['support_contacts'] + st.session_state.session_data['support_calls']
            st.write(f"Total: {total_support} (Base: {profile['support_contacts']}, Today: {st.session_state.session_data['support_calls']})")
        with col_btn4:
            if st.button("Contact", key="contact_support"):
                st.session_state.session_data['support_calls'] += 1
                
                # Support escalation warnings with limits
                if st.session_state.session_data['support_calls'] >= VALIDATION_LIMITS['MAX_SUPPORT_CALLS']:
                    st.error("🚨 Maximum support contacts reached for today")
                    return
                
                new_total = profile['support_contacts'] + st.session_state.session_data['support_calls']
                if st.session_state.session_data['support_calls'] > 3:
                    st.error(f"🚨 High support frequency: {st.session_state.session_data['support_calls']} calls today")
                elif new_total > 10:
                    st.warning(f"⚠️ Total support contacts: {new_total}")
                
                st.success(f"✅ Support contacted")
                st.rerun()
        
        # Reset - FIXED: Proper reset to zero balance
        if st.button("🔄 Reset"):
            current_customer = st.session_state.session_data['customer']
            current_profile = CUSTOMERS[current_customer]
            st.session_state.session_data = {
                'customer': current_customer,
                'balance': 0.0,  # Reset to zero balance
                'wagered': 0,
                'session_time': current_profile['avg_session'],
                'location': 'Home',
                'support_calls': 0,
                'deposits': [],
                'wagers': [],
                'location_history': []
            }
            st.success("✅ Session reset - Balance cleared")
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'><h3 style='font-family: Mulish, sans-serif; font-weight: 600; color: #8F00BF;'>🤖 ML Risk Assessment</h3>", unsafe_allow_html=True)
        
        # Risk Gauge
        risk_score = risk_result['score']
        needle_angle = -90 + (risk_score * 1.8)
        
        # Enhanced color coding based on risk levels
        if risk_score >= 80:
            gauge_color = "#dc2626"  # Critical Red
            text_color = "#dc2626"
            gauge_bg = "conic-gradient(from 180deg, #fca5a5 0deg, #f87171 45deg, #ef4444 90deg, #dc2626 135deg, #991b1b 180deg)"
        elif risk_score >= 60:
            gauge_color = "#f59e0b"  # High Orange
            text_color = "#f59e0b"
            gauge_bg = "conic-gradient(from 180deg, #fed7aa 0deg, #fdba74 60deg, #fb923c 120deg, #f59e0b 180deg)"
        elif risk_score >= 40:
            gauge_color = "#eab308"  # Medium Yellow
            text_color = "#eab308"
            gauge_bg = "conic-gradient(from 180deg, #fef3c7 0deg, #fde68a 90deg, #eab308 180deg)"
        else:
            gauge_color = "#22c55e"  # Low Green
            text_color = "#22c55e"
            gauge_bg = "conic-gradient(from 180deg, #bbf7d0 0deg, #86efac 90deg, #22c55e 180deg)"
        
        st.markdown(f"""
        <div style='text-align: center; margin: 2rem 0;'>
            <div style='width: 180px; height: 90px; margin: 0 auto; position: relative; overflow: hidden;'>
                <div style='position: absolute; width: 180px; height: 180px; border-radius: 50%; background: {gauge_bg}; top: 0; left: 0;'></div>
                <div style='position: absolute; width: 140px; height: 140px; border-radius: 50%; background: white; top: 20px; left: 20px;'></div>
                <div style='position: absolute; width: 3px; height: 70px; background: {gauge_color}; top: 20px; left: 50%; transform-origin: bottom center; transform: translateX(-50%) rotate({needle_angle}deg); z-index: 10;'></div>
            </div>
            <div style='font-size: 2.5rem; font-weight: 800; margin: 1rem 0; color: {text_color};'>{risk_score}</div>
            <div style='font-size: 1.2rem; font-weight: 600; color: {text_color};'>
                {risk_result['level']}: {risk_score}%
            </div>
            <div style='font-size: 0.9rem; color: #6b7280; margin-top: 0.5rem;'>
                🤖 AI Confidence: {ai_confidence:.1f}%<br>
                📅 Estimated Crisis: {days_to_crisis} days
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # AI-Enhanced Risk Breakdown
        st.markdown("<div style='margin-top: 2rem;'>", unsafe_allow_html=True)
        st.markdown("<div style='font-weight: 600; margin-bottom: 1rem; color: #8F00BF; font-family: Mulish, sans-serif;'>🤖 ML Risk Analysis:</div>", unsafe_allow_html=True)
        
        for factor, score in risk_result['factors'].items():
            color = "#dc2626" if score >= 20 else "#f59e0b" if score >= 15 else "#3b82f6" if score >= 10 else "#10b981"
            width = (score / 25) * 100
            
            st.markdown(f"""
            <div style='display: flex; align-items: center; margin: 1rem 0;'>
                <div style='min-width: 80px; font-size: 0.9rem; font-weight: 600;'>{factor}</div>
                <div style='flex: 1; height: 8px; background: #f3f4f6; border-radius: 4px; margin: 0 1rem; overflow: hidden;'>
                    <div style='height: 100%; width: {width}%; background: {color}; border-radius: 4px;'></div>
                </div>
                <div style='min-width: 40px; font-size: 0.9rem; font-weight: 600; text-align: right;'>{score}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='card'><h3 style='font-family: Mulish, sans-serif; font-weight: 600; color: #8F00BF;'>🤖 ML Interventions</h3>", unsafe_allow_html=True)
        
        interventions = get_interventions(risk_result, profile)
        
        if interventions:
            st.markdown("<div style='margin-bottom: 1rem; font-weight: 600; color: #8F00BF; font-family: Mulish, sans-serif;'>🤖 ML Recommended Actions:</div>", unsafe_allow_html=True)
            
            # Add AI confidence for interventions
            st.markdown(f"<div style='font-size: 0.8rem; color: #8F00BF; margin-bottom: 1rem; font-family: Mulish, sans-serif;'>{ml_status} | Confidence: {ai_confidence:.1f}% | Risk: {crisis_probability:.0f}%</div>", unsafe_allow_html=True)
            
            for i, intervention in enumerate(interventions):
                urgency_color = "#dc2626" if intervention['urgency'] == 'HIGH' else "#f59e0b"
                
                st.markdown(f"""
                <div style='border: 2px solid {urgency_color}; border-radius: 8px; padding: 1rem; margin: 1rem 0;'>
                    <div style='display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;'>
                        <span style='font-weight: 700;'>{intervention['type']}</span>
                        <span style='background: {urgency_color}; color: white; padding: 0.2rem 0.4rem; border-radius: 4px; font-size: 0.7rem;'>{intervention['urgency']}</span>
                    </div>
                    <div style='font-size: 0.85rem; color: #6b7280;'>{intervention['action']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"🤖 Execute {intervention['type']}", key=f"exec_{i}"):
                    # Track AI-driven intervention execution
                    if 'executed_interventions' not in st.session_state.session_data:
                        st.session_state.session_data['executed_interventions'] = []
                    
                    st.session_state.session_data['executed_interventions'].append({
                        'type': intervention['type'],
                        'timestamp': datetime.now().strftime('%H:%M:%S'),
                        'urgency': intervention['urgency'],
                        'ai_confidence': ai_confidence,
                        'crisis_probability': crisis_probability
                    })
                    
                    st.success(f"✅ ML-driven {intervention['type']} executed! Enhanced monitoring active.")
                    st.info(f"🤖 ML Intervention logged | {ml_status} | Confidence: {ai_confidence:.1f}%")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
        else:
            st.markdown(f"""
            <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); border-radius: 12px; border: 2px solid #10b981;'>
                <div style='font-size: 3rem; margin-bottom: 1rem;'>🤖✅</div>
                <h3 style='margin: 0; color: #10b981;'>AI All Clear!</h3>
                <p style='margin: 0.5rem 0 0 0; color: #059669;'>Customer within safe parameters</p>
                <p style='margin: 0.5rem 0 0 0; color: #059669; font-size: 0.9rem;'>{ml_status} | Confidence: {ai_confidence:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(page_title="Customer DNA AI", page_icon="🧬", layout="wide")
    main()
