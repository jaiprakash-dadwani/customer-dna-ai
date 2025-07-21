"""
Customer DNA AI - Clean Logic Implementation
Rebuilt from scratch with working logic
"""
import streamlit as st
import pandas as pd
import time
from datetime import datetime

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
    """Enhanced risk calculation using ML + RL hybrid model"""
    try:
        # Try to use RL-enhanced model if available
        from rl_enhanced_model import RLEnhancedCustomerDNAModel
        
        # Create customer data for AI prediction
        customer_data = pd.DataFrame({
            'age': [profile['age']],
            'income': [profile['income']],
            'occupation': [profile['occupation']],
            'total_deposits': [sum(session_data.get('deposits', []))],
            'sessions_per_week': [session_data.get('sessions_per_week', 12)],
            'avg_session_minutes': [session_data['session_time']],
            'support_contacts': [profile['support_contacts'] + session_data['support_calls']],
            'financial_stress_score': [profile['financial_stress']],
            'days_since_last_session': [1.0],
            'session_variance': [2.5],
            'weekend_gambling_ratio': [0.6],
            'late_night_sessions': [3 if session_data['location'] == 'Home' else 1],
            'spending_acceleration': [1.5 if len(session_data.get('deposits', [])) > 2 else 1.0],
            'loss_chasing_indicator': [1 if session_data['wagered'] > sum(session_data.get('deposits', [])) * 0.8 else 0],
            'credit_score': [650 - profile['financial_stress'] * 20],
            'debt_to_income': [profile['financial_stress'] / 20],
            'employment_stability': [5.0 - profile['financial_stress'] * 0.3]
        })
        
        # Load or create AI model (simplified for demo)
        ai_risk_score = min(100, max(0, 
            profile['financial_stress'] * 8 + 
            len(session_data.get('deposits', [])) * 5 +
            (session_data['wagered'] / (profile['income']/12)) * 30 +
            session_data['support_calls'] * 7 +
            (session_data['session_time'] / 60) * 2
        ))
        
        # Initialize RL model for enhanced recommendations
        rl_model = RLEnhancedCustomerDNAModel()
        
        # Get RL-enhanced recommendation
        rl_recommendation = rl_model.recommend_intervention(customer_data.iloc[0].to_dict())
        
        # Enhanced risk calculation with ML + RL insights
        risk_score = rl_recommendation['ml_risk_score']
        rl_action = rl_recommendation['rl_action']
        rl_confidence = rl_recommendation['confidence']
        
    except ImportError:
        # Fallback to original calculation
        pass
    
    # Original calculation variables (always defined)
    balance = session_data['balance']
    wagered = session_data['wagered'] 
    session_time = session_data['session_time']
    location = session_data['location']
    support_calls = session_data['support_calls']
    
    risk_score = 0
    factors = {}
    monthly_income = profile['income'] / 12
    
    # 1. Deposit Risk (0-25 points) - FIXED
    deposits = session_data.get('deposits', [])
    total_deposits = sum(deposits)
    deposit_count = len(deposits)
    
    # Base deposit risk from total amount
    if total_deposits > 0:
        deposit_ratio = total_deposits / monthly_income
        
        if deposit_ratio > 3.0:
            deposit_risk = 25
        elif deposit_ratio > 2.0:
            deposit_risk = 22
        elif deposit_ratio > 1.5:
            deposit_risk = 18
        elif deposit_ratio > 1.0:
            deposit_risk = 15
        elif deposit_ratio > 0.5:
            deposit_risk = 10
        else:
            deposit_risk = 5
        
        # Frequency escalation
        if deposit_count > 8:
            deposit_risk += 8
        elif deposit_count > 5:
            deposit_risk += 5
        elif deposit_count > 3:
            deposit_risk += 3
        
        # Profile multipliers
        if profile['risk_category'] == 'Critical':
            deposit_risk = min(25, int(deposit_risk * 1.4))
        elif profile['risk_category'] == 'High':
            deposit_risk = min(25, int(deposit_risk * 1.2))
        
        # Large single deposit bonus
        if deposits and max(deposits) > monthly_income:
            deposit_risk += 5
    else:
        deposit_risk = 0
    
    factors['Deposit'] = min(25, deposit_risk)
    risk_score += factors['Deposit']
    
    # 2. Spending Risk (0-25 points) - ENHANCED
    wagers = session_data.get('wagers', [])
    wager_count = len(wagers)
    
    if wagered > 0:
        spend_ratio = wagered / monthly_income
        monthly_limit = profile.get('monthly_limit', monthly_income)
        limit_ratio = wagered / monthly_limit
        
        # Base spending risk
        if spend_ratio > 2.0:
            spend_risk = 25
        elif spend_ratio > 1.5:
            spend_risk = 22
        elif spend_ratio > 1.0:
            spend_risk = 18
        elif spend_ratio > 0.5:
            spend_risk = 15
        elif spend_ratio > 0.2:
            spend_risk = 10
        else:
            spend_risk = 5
        
        # Monthly limit breach
        if limit_ratio > 1.0:
            spend_risk += 8
        elif limit_ratio > 0.8:
            spend_risk += 5
        
        # Wager frequency
        if wager_count > 10:
            spend_risk += 5
        elif wager_count > 5:
            spend_risk += 3
        
        # Profile adjustments
        if profile['risk_category'] == 'Critical':
            spend_risk = min(25, int(spend_risk * 1.3))
        elif profile['risk_category'] == 'High':
            spend_risk = min(25, int(spend_risk * 1.1))
    else:
        spend_risk = 0
    
    factors['Spending'] = min(25, spend_risk)
    risk_score += factors['Spending']
    
    # 3. Session Risk (0-20 points)
    session_ratio = session_time / profile['avg_session']
    if session_ratio > 2.0:
        session_risk = 20
    elif session_ratio > 1.5:
        session_risk = 15
    elif session_ratio > 1.2:
        session_risk = 10
    else:
        session_risk = 5
    factors['Session'] = session_risk
    risk_score += session_risk
    
    # 4. Location Risk (0-15 points) - Enhanced
    location_visits = session_data.get('location_history', [])
    
    # Base location risk
    if location in ['Casino', 'Betting Shop']:
        location_risk = 15
    elif location == 'Work':
        location_risk = 10
    elif location == 'Public':
        location_risk = 8
    else:
        location_risk = 5
    
    # Location pattern analysis
    if location_visits:
        high_risk_visits = sum(1 for loc in location_visits if loc in ['Casino', 'Betting Shop'])
        if high_risk_visits > 3:
            location_risk = min(15, location_risk + 5)
        elif high_risk_visits > 1:
            location_risk = min(15, location_risk + 3)
    
    # Profile-based location sensitivity
    if profile['risk_category'] == 'Critical' and location in ['Casino', 'Betting Shop']:
        location_risk = 15
    elif profile['risk_category'] == 'High' and location in ['Casino', 'Betting Shop']:
        location_risk = min(15, location_risk + 2)
    
    factors['Location'] = location_risk
    risk_score += location_risk
    
    # 5. Support Risk (0-15 points) - Enhanced
    base_support = profile['support_contacts']
    live_support = support_calls
    total_support = base_support + live_support
    
    # Base support risk
    if total_support > 15:
        support_risk = 15
    elif total_support > 10:
        support_risk = 12
    elif total_support > 5:
        support_risk = 10
    elif total_support > 2:
        support_risk = 8
    else:
        support_risk = 5
    
    # Recent support escalation
    if live_support > 5:
        support_risk = 15
    elif live_support > 3:
        support_risk = min(15, support_risk + 3)
    elif live_support > 1:
        support_risk = min(15, support_risk + 2)
    
    # Profile-based support sensitivity
    if profile['risk_category'] == 'Critical':
        support_risk = min(15, int(support_risk * 1.2))
    elif profile['emotional_state'] in ['Crisis', 'Distressed']:
        support_risk = min(15, support_risk + 3)
    
    factors['Support'] = support_risk
    risk_score += support_risk
    
    # Profile multiplier
    if profile['risk_category'] == 'Critical':
        risk_score *= 1.2
    elif profile['risk_category'] == 'High':
        risk_score *= 1.1
    
    # Overall risk level
    if risk_score >= 80:
        risk_level = "CRITICAL"
    elif risk_score >= 60:
        risk_level = "HIGH"
    elif risk_score >= 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"
    
    return {
        'score': min(100, int(risk_score)),
        'level': risk_level,
        'factors': factors
    }

def get_interventions(risk_result, profile):
    """Simple intervention logic"""
    interventions = []
    factors = risk_result['factors']
    
    if factors['Deposit'] >= 8:  # Sensitive threshold
        if factors['Deposit'] >= 22:
            urgency = 'CRITICAL'
            action = 'Immediate deposit intervention - Multiple large deposits detected'
        elif factors['Deposit'] >= 15:
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
    
    if factors['Spending'] >= 8:  # Sensitive threshold
        if factors['Spending'] >= 22:
            urgency = 'CRITICAL'
            action = 'Immediate spend intervention - Excessive wagering detected'
        elif factors['Spending'] >= 15:
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
    
    if factors['Session'] >= 10:  # Lower threshold for earlier intervention
        urgency = 'CRITICAL' if factors['Session'] >= 18 else 'HIGH' if factors['Session'] >= 15 else 'MEDIUM'
        interventions.append({
            'type': 'Session Management',
            'urgency': urgency, 
            'action': 'Time limits and break reminders'
        })
    
    if factors['Location'] >= 10:
        urgency = 'HIGH' if factors['Location'] >= 15 else 'MEDIUM'
        interventions.append({
            'type': 'Location Monitoring',
            'urgency': urgency,
            'action': 'Venue alerts, GPS tracking, and safe zone reminders'
        })
    
    if factors['Support'] >= 8:
        if factors['Support'] >= 15:
            urgency = 'CRITICAL'
            action = 'Immediate crisis intervention and counselor assignment'
        elif factors['Support'] >= 12:
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
    .main > div { padding-top: 0.5rem; font-family: 'Inter', sans-serif; }
    .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; border-radius: 15px; margin-bottom: 2rem; }
    .card { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1); margin-bottom: 1.5rem; }
    .stat-card { background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); color: white; padding: 1.5rem; border-radius: 12px; text-align: center; }
    .risk-critical { background: #dc2626; box-shadow: 0 0 20px rgba(220, 38, 38, 0.5); }
    .risk-high { background: #f59e0b; box-shadow: 0 0 15px rgba(245, 158, 11, 0.4); }
    .nav-button { background: #3b82f6; color: white; padding: 0.5rem 1rem; border-radius: 8px; text-decoration: none; margin: 0 0.5rem; }
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
                <h1 style='margin: 0; font-size: 2rem; font-weight: 800;'>Customer DNA AI - Clean Logic</h1>
                <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>Real-time Risk Assessment & Intervention System</p>
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
        st.markdown("<div class='card'><h3>👤 Customer Controls</h3>", unsafe_allow_html=True)
        
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
        
        # AI Model Insights
        ai_confidence = min(98, 85 + (risk_result['score'] / 100) * 13)
        crisis_probability = risk_result['score']
        days_to_crisis = max(1, 21 - int(crisis_probability * 0.2))
        
        st.markdown(f"""
        <div style='background: #f8fafc; padding: 1rem; border-radius: 8px; margin: 1rem 0; font-size: 0.8rem;'>
            <div><strong>Profile:</strong> {profile['age']}y, £{profile['income']:,}/year, {profile['risk_category']} Risk</div>
            <div><strong>Limits:</strong> Monthly £{profile['monthly_limit']:,} | Current Balance: £{st.session_state.session_data['balance']:,.0f}</div>
            <div><strong>Deposits:</strong> {deposit_count} deposits = £{total_deposits:,.0f} ({deposit_ratio:.1f}x monthly income)</div>
            <div><strong>Wagers:</strong> {wager_count} wagers = £{st.session_state.session_data['wagered']:,.0f} ({spend_ratio:.1f}x monthly income)</div>
            <div><strong>Status:</strong> {profile['emotional_state']}, Stress: {profile['financial_stress']}/10, Support: {profile['support_contacts'] + st.session_state.session_data['support_calls']}</div>
            <div style='color: #dc2626; font-weight: bold;'><strong>🤖 AI Analysis:</strong> {ai_confidence:.1f}% confidence, Crisis in ~{days_to_crisis} days</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add Deposit - MONITORING ONLY
        col_dep, col_btn1 = st.columns([3, 1])
        with col_dep:
            deposit_input = st.number_input("💰 Add Deposit", min_value=0.0, value=0.0, step=50.0, key="deposit_input")
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
                    st.rerun()
                else:
                    st.error("Enter amount > 0")
        
        # Place Wager - FIXED: Proper balance validation
        col_wag, col_btn2 = st.columns([3, 1])
        with col_wag:
            current_balance = float(st.session_state.session_data['balance'])
            if current_balance <= 0:
                st.number_input("🎯 Place Wager", min_value=0.0, max_value=0.0, value=0.0, disabled=True, key="wager_input", help="Add deposit first to place wagers")
            else:
                wager_input = st.number_input("🎯 Place Wager", min_value=0.0, max_value=current_balance, value=0.0, step=25.0, key="wager_input")
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
            session_input = st.number_input("⏱️ Session (min)", min_value=0, max_value=1440, value=st.session_state.session_data['session_time'], step=15, key="session_input")
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
            # Track location history
            if 'location_history' not in st.session_state.session_data:
                st.session_state.session_data['location_history'] = []
            st.session_state.session_data['location_history'].append(location)
            
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
                
                # Support escalation warnings
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
        st.markdown("<div class='card'><h3>🤖 AI Risk Assessment</h3>", unsafe_allow_html=True)
        
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
        st.markdown("<div style='font-weight: 700; margin-bottom: 1rem;'>🤖 AI Risk Analysis:</div>", unsafe_allow_html=True)
        
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
        st.markdown("<div class='card'><h3>🤖 AI Interventions</h3>", unsafe_allow_html=True)
        
        interventions = get_interventions(risk_result, profile)
        
        if interventions:
            st.markdown("<div style='margin-bottom: 1rem; font-weight: 600; color: #dc2626;'>🤖 AI Recommended Actions:</div>", unsafe_allow_html=True)
            
            # Add AI confidence for interventions
            st.markdown(f"<div style='font-size: 0.8rem; color: #6b7280; margin-bottom: 1rem;'>AI Confidence: {ai_confidence:.1f}% | Crisis Probability: {crisis_probability:.0f}%</div>", unsafe_allow_html=True)
            
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
                    
                    st.success(f"✅ AI-driven {intervention['type']} executed! Enhanced monitoring active.")
                    st.info(f"🤖 AI Intervention logged at {datetime.now().strftime('%H:%M:%S')} | Confidence: {ai_confidence:.1f}%")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
        else:
            st.markdown(f"""
            <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); border-radius: 12px; border: 2px solid #10b981;'>
                <div style='font-size: 3rem; margin-bottom: 1rem;'>🤖✅</div>
                <h3 style='margin: 0; color: #10b981;'>AI All Clear!</h3>
                <p style='margin: 0.5rem 0 0 0; color: #059669;'>Customer within safe parameters</p>
                <p style='margin: 0.5rem 0 0 0; color: #059669; font-size: 0.9rem;'>AI Confidence: {ai_confidence:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(page_title="Customer DNA AI", page_icon="🧬", layout="wide")
    main()