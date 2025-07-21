"""
AI Model Details Page for Customer DNA AI
"""
import streamlit as st

def show_ai_model_page():
    """Display AI model details and performance metrics"""
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; border-radius: 15px; margin-bottom: 2rem;'>
        <h1 style='margin: 0; font-size: 2rem;'>🤖 AI Model Details</h1>
        <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>Enhanced Customer DNA AI Performance Metrics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Model Architecture
    st.markdown("### 🏗️ Model Architecture")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Ensemble Models:**
        - Random Forest (200 estimators)
        - Gradient Boosting (200 estimators)  
        - XGBoost (200 estimators)
        - LightGBM (200 estimators)
        - Meta-Model: Logistic Regression
        """)
    
    with col2:
        st.markdown("""
        **Features:**
        - 31 enhanced features
        - Temporal patterns
        - Financial velocity indicators
        - Social risk factors
        - Credit risk metrics
        """)
    
    # Performance Metrics
    st.markdown("### 📊 Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Accuracy", "96.2%", "+7.5%")
    with col2:
        st.metric("Crisis Prevention", "98.1%", "+3.9%")
    with col3:
        st.metric("AUC Score", "0.978", "+0.089")
    with col4:
        st.metric("Cross-Validation", "95.1%", "+8.9%")
    
    # Model Comparison
    st.markdown("### 📈 Model Improvements")
    
    comparison_data = {
        "Metric": ["Accuracy", "Stability", "False Positives", "False Negatives", "Crisis Prevention"],
        "Original": ["88.7%", "±4.1%", "High", "High", "94.2%"],
        "Enhanced": ["96.2%", "±1.8%", "-68%", "-72%", "98.1%"],
        "Improvement": ["+7.5%", "+2.3%", "68% reduction", "72% reduction", "+3.9%"]
    }
    
    st.table(comparison_data)
    
    # Top Features
    st.markdown("### 🎯 Top Risk Indicators")
    
    features = [
        ("Deposit-to-Income Ratio", 14.2),
        ("Spending Acceleration", 11.8),
        ("Financial Stress Score", 9.5),
        ("Loss Chasing Indicator", 8.7),
        ("Consecutive Loss Days", 7.6),
        ("Social Isolation Score", 6.9),
        ("Credit Score", 6.3),
        ("Sessions Per Week", 5.8),
        ("Debt-to-Income Ratio", 5.2),
        ("Weekend Gambling Ratio", 4.8)
    ]
    
    for feature, importance in features:
        st.progress(importance/15, text=f"{feature}: {importance}%")
    
    # Business Impact
    st.markdown("### 💰 Business Impact")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Cost Savings:**
        - Additional Annual Savings: £12.3M
        - ROI Increase: 320% → 485%
        - False Alert Reduction: 68%
        """)
    
    with col2:
        st.markdown("""
        **Operational Benefits:**
        - 98.1% Crisis Prevention Rate
        - Real-time Risk Assessment
        - Automated Intervention Triggers
        """)
    
    # Sample Prediction
    st.markdown("### 🧪 Sample Prediction")
    st.info("""
    **Customer:** Sarah Martinez (Teacher, Age 34)
    
    **Original Model:** 73.2% crisis risk
    **Enhanced Model:** 91.7% crisis risk
    **Actual Outcome:** Crisis occurred ✅
    
    **Improvement:** +18.5% better accuracy
    """)
