import streamlit as st
import re
import string
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Advanced Password Strength Analyzer",
    page_icon="🔒",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #ff0000, #ffa500, #ffff00, #008000);
    }
    </style>
""", unsafe_allow_html=True)

def analyze_password_strength(password):
    score = 0
    feedback = []
    strength_details = {}
    
    # Basic checks
    length_score = min(len(password) / 12, 1.0)  # Normalize length score
    score += length_score * 2  # Length carries more weight
    strength_details['Length'] = f"{len(password)} characters ({int(length_score * 100)}%)"
    
    if len(password) < 8:
        feedback.append("🚫 Password length kam se kam 8 characters hona chahiye")
    elif len(password) < 12:
        feedback.append("💡 12+ characters ke password zyada secure hote hain")
    
    # Character variety checks
    patterns = {
        'uppercase': (r'[A-Z]', "Capital letters (A-Z)"),
        'lowercase': (r'[a-z]', "Small letters (a-z)"),
        'numbers': (r'\d', "Numbers (0-9)"),
        'special': (r'[!@#$%^&*(),.?":{}|<>]', "Special characters")
    }
    
    for check, (pattern, desc) in patterns.items():
        matches = len(re.findall(pattern, password))
        if matches > 0:
            score += min(matches / 3, 1.0)  # Cap the score contribution
            strength_details[desc] = f"{matches} found"
        else:
            feedback.append(f"🚫 {desc} ka use karein")
    
    # Advanced checks
    if not any(c1 == c2 for c1, c2 in zip(password[:-1], password[1:])):
        score += 1
        strength_details['Repetition'] = "No repeated characters"
    else:
        feedback.append("⚠️ Repeating characters ka use na karein")
    
    # Common patterns check
    common_patterns = ['123', 'abc', 'qwerty', 'password']
    if not any(pattern.lower() in password.lower() for pattern in common_patterns):
        score += 1
    else:
        feedback.append("⚠️ Common patterns ka use na karein")
    
    # Normalize final score to 0-100
    final_score = min(score * 10, 100)
    
    return final_score, feedback, strength_details

def main():
    st.title("🔒 Professional Password Strength Analyzer")
    st.markdown("---")
    
    password = st.text_input(
        "Enter your password:",
        type="password",
        help="Enter the password you want to analyze"
    )
    
    if password:
        score, feedback, details = analyze_password_strength(password)
        
        # Display score
        st.markdown(f"### Strength Score: {int(score)}%")
        st.progress(score/100)
        
        # Display strength level with color coding
        if score >= 80:
            st.success("🔒 VERY STRONG - Excellent Password!")
        elif score >= 60:
            st.info("🔐 STRONG - Good Password")
        elif score >= 40:
            st.warning("⚠️ MODERATE - Password can be improved")
        else:
            st.error("⛔ WEAK - Password needs significant improvement")
        
        # Display detailed analysis
        st.markdown("### Detailed Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Password Properties")
            for key, value in details.items():
                st.write(f"**{key}:** {value}")
        
        with col2:
            if feedback:
                st.markdown("#### Improvement Suggestions")
                for suggestion in feedback:
                    st.write(suggestion)
        
        # Security tips
        with st.expander("📌 Password Security Tips"):
            st.markdown("""
            - Use a mix of characters, numbers, and symbols
            - Avoid personal information
            - Use different passwords for different accounts
            - Consider using a password manager
            - Enable two-factor authentication when possible
            """)

if __name__ == "__main__":
    main()