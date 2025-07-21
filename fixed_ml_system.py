"""
Fixed ML System - Actually learns from data, no hardcoded rules
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
import joblib
import os
from datetime import datetime

class FixedCustomerRiskML:
    def __init__(self):
        self.model = Ridge(alpha=0.1, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self.training_data = []
        self.model_path = 'fixed_risk_model.pkl'
        self.scaler_path = 'fixed_scaler.pkl'
        self.data_path = 'fixed_training_data.pkl'
        
        # Comprehensive features that work together for ML decisions
        self.feature_names = [
            'age', 'income', 'financial_stress', 'total_deposits', 'total_wagered',
            'session_time', 'support_calls', 'deposit_count', 'wager_count', 'location_risk',
            'profession_risk', 'work_stress_level', 'deposit_to_income_ratio', 'wager_to_income_ratio',
            'wager_to_deposit_ratio', 'session_intensity', 'gambling_frequency', 'support_escalation', 'risk_amplifier'
        ]
        
        # Initialize with realistic training data
        self._initialize_training_data()
        
    def _initialize_training_data(self):
        """Initialize with realistic training samples"""
        # Low risk samples (Small amounts, stable behavior, good ratios)
        for _ in range(25):
            deposits = np.random.randint(20, 150)
            wagered = np.random.randint(10, min(80, deposits))  # Can't wager more than deposited
            income = np.random.randint(40000, 90000)
            monthly_income = income / 12
            
            sample = {
                'age': np.random.randint(25, 60),
                'income': income,
                'financial_stress': np.random.randint(1, 3),
                'total_deposits': deposits,
                'total_wagered': wagered,
                'session_time': np.random.randint(30, 90),
                'support_calls': np.random.randint(0, 1),
                'deposit_count': np.random.randint(1, 2),
                'wager_count': np.random.randint(1, 2),
                'location_risk': 5,
                'profession_risk': np.random.choice([4, 5]),
                'work_stress_level': np.random.randint(2, 4),
                # Interconnected features for low risk
                'deposit_to_income_ratio': deposits / monthly_income,
                'wager_to_income_ratio': wagered / monthly_income,
                'wager_to_deposit_ratio': wagered / deposits if deposits > 0 else 0,
                'session_intensity': np.random.uniform(0.5, 1.2),
                'gambling_frequency': np.random.randint(2, 4),
                'support_escalation': np.random.uniform(0, 0.5),
                'risk_amplifier': np.random.uniform(1.0, 1.2),
                'target_risk_score': np.random.randint(15, 30),
                'timestamp': datetime.now().isoformat()
            }
            self.training_data.append(sample)
        
        # Medium risk samples (Moderate amounts, concerning ratios)
        for _ in range(15):
            deposits = np.random.randint(150, 500)
            wagered = np.random.randint(80, min(400, deposits))
            income = np.random.randint(45000, 80000)
            monthly_income = income / 12
            
            sample = {
                'age': np.random.randint(30, 55),
                'income': income,
                'financial_stress': np.random.randint(3, 6),
                'total_deposits': deposits,
                'total_wagered': wagered,
                'session_time': np.random.randint(90, 180),
                'support_calls': np.random.randint(1, 3),
                'deposit_count': np.random.randint(2, 4),
                'wager_count': np.random.randint(2, 5),
                'location_risk': np.random.choice([5, 10]),
                'profession_risk': 4,
                'work_stress_level': np.random.randint(4, 6),
                # Interconnected features for medium risk
                'deposit_to_income_ratio': deposits / monthly_income,
                'wager_to_income_ratio': wagered / monthly_income,
                'wager_to_deposit_ratio': wagered / deposits if deposits > 0 else 0,
                'session_intensity': np.random.uniform(1.0, 2.0),
                'gambling_frequency': np.random.randint(4, 8),
                'support_escalation': np.random.uniform(0.3, 1.0),
                'risk_amplifier': np.random.uniform(1.2, 1.8),
                'target_risk_score': np.random.randint(35, 55),
                'timestamp': datetime.now().isoformat()
            }
            self.training_data.append(sample)
        
        # High risk samples (Large amounts, dangerous ratios, multiple risk factors)
        for _ in range(10):
            deposits = np.random.randint(500, 1500)
            wagered = np.random.randint(400, min(1400, deposits))
            income = np.random.randint(20000, 45000)
            monthly_income = income / 12
            
            sample = {
                'age': np.random.randint(25, 45),
                'income': income,
                'financial_stress': np.random.randint(7, 10),
                'total_deposits': deposits,
                'total_wagered': wagered,
                'session_time': np.random.randint(240, 480),
                'support_calls': np.random.randint(5, 15),
                'deposit_count': np.random.randint(4, 10),
                'wager_count': np.random.randint(6, 15),
                'location_risk': np.random.choice([10, 15]),
                'profession_risk': np.random.choice([7, 9]),
                'work_stress_level': np.random.randint(7, 10),
                # Interconnected features for high risk (dangerous combinations)
                'deposit_to_income_ratio': deposits / monthly_income,
                'wager_to_income_ratio': wagered / monthly_income,
                'wager_to_deposit_ratio': wagered / deposits if deposits > 0 else 0,
                'session_intensity': np.random.uniform(2.0, 4.0),
                'gambling_frequency': np.random.randint(8, 20),
                'support_escalation': np.random.uniform(1.0, 3.0),
                'risk_amplifier': np.random.uniform(1.8, 3.0),
                'target_risk_score': np.random.randint(65, 90),
                'timestamp': datetime.now().isoformat()
            }
            self.training_data.append(sample)
        
        # Train initial model
        self.train_model()
    
    def extract_features(self, profile, session_data):
        """Extract comprehensive features that work together for ML decisions"""
        deposits = session_data.get('deposits', [])
        wagers = session_data.get('wagers', [])
        monthly_income = profile['income'] / 12
        
        # Map profession to risk level
        profession_risk_map = {
            'Teacher': 7,  # High stress, low income
            'Executive': 4,  # Medium stress, good income
            'Business Owner': 9  # High stress, irregular income
        }
        
        # Map work stress to numeric
        work_stress_map = {
            'Low': 2, 'Medium': 5, 'High': 7, 'Very High': 9, 'Extreme': 10
        }
        
        # Calculate derived features that connect all inputs
        total_deposits = sum(deposits)
        total_wagered = session_data['wagered']
        
        # Financial ratios (key ML features)
        deposit_to_income = total_deposits / monthly_income if monthly_income > 0 else 0
        wager_to_income = total_wagered / monthly_income if monthly_income > 0 else 0
        wager_to_deposit = total_wagered / total_deposits if total_deposits > 0 else 0
        
        # Behavioral patterns
        session_intensity = session_data['session_time'] / profile['avg_session'] if profile['avg_session'] > 0 else 1
        gambling_frequency = len(deposits) + len(wagers)
        support_escalation = session_data['support_calls'] / max(1, profile['support_contacts'])
        
        # Risk amplifiers (when multiple factors combine)
        location_multiplier = 1.5 if session_data['location'] in ['Casino', 'Betting Shop'] else 1.2 if session_data['location'] == 'Work' else 1.0
        stress_multiplier = 1 + (profile['financial_stress'] / 20)
        
        features = {
            'age': profile['age'],
            'income': profile['income'],
            'financial_stress': profile['financial_stress'],
            'total_deposits': total_deposits,
            'total_wagered': total_wagered,
            'session_time': session_data['session_time'],
            'support_calls': profile['support_contacts'] + session_data['support_calls'],
            'deposit_count': len(deposits),
            'wager_count': len(wagers),
            'location_risk': 15 if session_data['location'] in ['Casino', 'Betting Shop'] else 10 if session_data['location'] == 'Work' else 5,
            'profession_risk': profession_risk_map.get(profile.get('profession', 'Other'), 5),
            'work_stress_level': work_stress_map.get(profile.get('work_stress', 'Medium'), 5),
            # New interconnected features
            'deposit_to_income_ratio': deposit_to_income,
            'wager_to_income_ratio': wager_to_income,
            'wager_to_deposit_ratio': wager_to_deposit,
            'session_intensity': session_intensity,
            'gambling_frequency': gambling_frequency,
            'support_escalation': support_escalation,
            'risk_amplifier': location_multiplier * stress_multiplier
        }
        
        return features
    
    def add_training_sample(self, profile, session_data, actual_risk_score=None):
        """Add new sample and retrain"""
        features = self.extract_features(profile, session_data)
        
        # If no actual score provided, get current ML prediction as baseline
        if actual_risk_score is None and self.is_trained:
            try:
                current_pred = self.predict_risk(profile, session_data)
                actual_risk_score = current_pred['risk_score']
            except:
                actual_risk_score = 50  # Default
        elif actual_risk_score is None:
            actual_risk_score = 50  # Default for first samples
        
        sample = {
            **features,
            'target_risk_score': actual_risk_score,
            'timestamp': datetime.now().isoformat()
        }
        
        self.training_data.append(sample)
        
        # Keep last 100 samples
        if len(self.training_data) > 100:
            self.training_data = self.training_data[-100:]
        
        # Retrain every 5 new samples
        if len(self.training_data) % 5 == 0:
            self.train_model()
    
    def train_model(self):
        """Train ML model on actual data"""
        if len(self.training_data) < 10:
            return False
        
        # Prepare data
        df = pd.DataFrame(self.training_data)
        X = df[self.feature_names]
        y = df['target_risk_score']
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled, y)
        self.is_trained = True
        
        # Save model
        self.save_model()
        
        return True
    
    def predict_risk(self, profile, session_data):
        """Predict using trained ML model only"""
        features = self.extract_features(profile, session_data)
        
        if not self.is_trained:
            return {
                'risk_score': 50,
                'confidence': 0.5,
                'method': 'default',
                'samples_used': len(self.training_data)
            }
        
        try:
            # Prepare features
            feature_values = [features[name] for name in self.feature_names]
            feature_scaled = self.scaler.transform([feature_values])
            
            # ML prediction only
            ml_score = self.model.predict(feature_scaled)[0]
            
            # Confidence based on training data
            confidence = min(0.95, 0.7 + (len(self.training_data) / 200))
            
            return {
                'risk_score': int(max(15, min(95, ml_score))),
                'confidence': confidence,
                'method': 'ml_only',
                'samples_used': len(self.training_data)
            }
            
        except Exception as e:
            return {
                'risk_score': 50,
                'confidence': 0.5,
                'method': 'error',
                'samples_used': len(self.training_data)
            }
    
    def save_model(self):
        """Save model"""
        try:
            if self.is_trained:
                joblib.dump(self.model, self.model_path)
                joblib.dump(self.scaler, self.scaler_path)
            joblib.dump(self.training_data, self.data_path)
            return True
        except:
            return False
    
    def load_model(self):
        """Load model"""
        try:
            if os.path.exists(self.data_path):
                self.training_data = joblib.load(self.data_path)
            
            if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
                self.is_trained = True
                return True
        except:
            pass
        return False

# Global fixed ML instance
fixed_ml = FixedCustomerRiskML()
fixed_ml.load_model()