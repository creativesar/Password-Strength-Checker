import streamlit as st
import re
import string
from datetime import datetime
import time
import hashlib
import zxcvbn
from typing import Tuple, List, Dict
import plotly.graph_objects as go

# Page configuration with modern theme
st.set_page_config(
    page_title="🛡️ Advanced Password Security Analyzer",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Modern UI
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background-color: #f8f9fa;
    }
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #dc3545, #ffc107, #17a2b8, #28a745);
    }
    .password-header {
        color: #1e1e1e;
        font-family: 'Segoe UI', sans-serif;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 5px;
    }
    .feedback-box {
        padding: 1rem;
        border-radius: 5px;
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

def create_strength_gauge(score: float) -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#007bff"},
            'steps': [
                {'range': [0, 40], 'color': "#dc3545"},
                {'range': [40, 60], 'color': "#ffc107"},
                {'range': [60, 80], 'color': "#17a2b8"},
                {'range': [80, 100], 'color': "#28a745"}
            ]
        },
        title={'text': "Password Strength"}
    ))
    fig.update_layout(height=250)
    return fig

def analyze_password_strength(password: str) -> Tuple[float, List[str], Dict]:
    score = 0
    feedback = []
    strength_details = {}
    
    # Use zxcvbn for advanced analysis
    zxcvbn_result = zxcvbn.zxcvbn(password)
    base_score = zxcvbn_result['score'] * 20  # Convert 0-4 scale to 0-100
    
    # Enhanced length analysis
    length_score = min(len(password) / 16, 1.0)
    score += length_score * 25
    strength_details['Length Analysis'] = {
        'score': int(length_score * 100),
        'details': f"{len(password)} characters"
    }
    
    # Entropy calculation
    entropy = len(set(password)) / len(password)
    entropy_score = entropy * 25
    score += entropy_score
    strength_details['Entropy Score'] = int(entropy_score)
    
    # Character variety analysis
    patterns = {
        'uppercase': (r'[A-Z]', "Capital Letters"),
        'lowercase': (r'[a-z]', "Small Letters"),
        'numbers': (r'\d', "Numbers"),
        'special': (r'[!@#$%^&*(),.?":{}|<>]', "Special Characters")
    }
    
    variety_score = 0
    for check, (pattern, desc) in patterns.items():
        matches = len(re.findall(pattern, password))
        if matches > 0:
            variety_score += 6.25  # Total 25 points for variety
            strength_details[desc] = matches
        else:
            feedback.append(f"🔍 Add {desc} to strengthen your password")
    
    score += variety_score
    
    # Advanced security checks
    if zxcvbn_result['feedback']['warning']:
        feedback.append(f"⚠️ {zxcvbn_result['feedback']['warning']}")
    
    # Final score calculation
    final_score = min((score + base_score) / 2, 100)
    
    return final_score, feedback, strength_details

def main():
    st.title("🛡️ Advanced Password Security Analyzer")
    st.markdown("<div class='password-header'>Modern Password Security Analysis Tool</div>", unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            password = st.text_input(
                "Enter your password:",
                type="password",
                help="Your password is analyzed locally and never stored"
            )
        
        with col2:
            st.markdown("### Real-time Analysis")
            if password:
                with st.spinner("Analyzing password strength..."):
                    time.sleep(0.5)  # Add slight delay for better UX
                    score, feedback, details = analyze_password_strength(password)
                    
                    # Display interactive gauge
                    st.plotly_chart(create_strength_gauge(score), use_container_width=True)
    
    if password:
        tab1, tab2, tab3 = st.tabs(["Detailed Analysis", "Security Suggestions", "Best Practices"])
        
        with tab1:
            st.markdown("### 📊 Strength Components")
            for key, value in details.items():
                st.metric(key, value if isinstance(value, (int, str)) else value['details'])
        
        with tab2:
            st.markdown("### 🔍 Security Feedback")
            for suggestion in feedback:
                st.info(suggestion)
        
        with tab3:
            st.markdown("""
            ### 🎯 Password Best Practices
            1. Use at least 12 characters
            2. Mix uppercase, lowercase, numbers, and symbols
            3. Avoid personal information
            4. Use unique passwords for each account
            5. Consider using a password manager
            6. Enable two-factor authentication
            """)

if __name__ == "__main__":
    main()