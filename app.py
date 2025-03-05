import streamlit as st
import re
from zxcvbn import zxcvbn
import time

# Page configuration
st.set_page_config(
    page_title="Modern Password Strength Checker",
    page_icon="🔒",
    layout="centered"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .stTextInput > div > div > input {
        font-size: 20px;
    }
    .main {
        padding: 2rem;
    }
    .css-1v0mbdj.etr89bj1 {
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>🔒 Password Strength Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2em;'>Check how strong your password is!</p>", unsafe_allow_html=True)

# Password input
password = st.text_input("Enter your password", type="password")

if password:
    # Get detailed password analysis using zxcvbn
    results = zxcvbn(password)
    
    # Calculate strength score
    score = results['score']
    
    # Create progress bar
    strength_colors = ['#DC143C', '#FF4500', '#FFA500', '#9ACD32', '#228B22']
    progress_bar = st.progress(0)
    progress_bar.progress((score + 1) * 20)
    
    # Display strength label
    strength_labels = ['Very Weak', 'Weak', 'Medium', 'Strong', 'Very Strong']
    st.markdown(f"<h3 style='text-align: center; color: {strength_colors[score]};'>{strength_labels[score]}</h3>", unsafe_allow_html=True)
    
    # Password analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Password Analysis")
        checks = {
            "Length (≥ 8)": len(password) >= 8,
            "Uppercase": bool(re.search(r'[A-Z]', password)),
            "Lowercase": bool(re.search(r'[a-z]', password)),
            "Numbers": bool(re.search(r'[0-9]', password)),
            "Special Chars": bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        }
        
        for check, passed in checks.items():
            icon = "✅" if passed else "❌"
            st.markdown(f"{icon} {check}")
    
    with col2:
        st.subheader("Suggestions")
        if results['feedback']['warning']:
            st.warning(results['feedback']['warning'])
        
        suggestions = results['feedback']['suggestions']
        if suggestions:
            for suggestion in suggestions:
                st.info(suggestion)
        else:
            st.success("Great job! Your password looks good!")
    
    # Crack time estimation
    st.subheader("Estimated Time to Crack")
    crack_time = results['crack_times_display']['offline_fast_hashing_1e10_per_second']
    st.markdown(f"<p style='font-size: 1.2em; color: #2E86C1;'>⏱️ {crack_time}</p>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>Made with ❤️ for security</p>", unsafe_allow_html=True)