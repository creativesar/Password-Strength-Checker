# ... existing imports ...
import streamlit as st
import re
import string
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Advanced Password Strength Analyzer",
    page_icon="🔒",
    layout="wide"  # Changed to wide layout
)

# Enhanced Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #ff0000, #ffa500, #ffff00, #008000);
    }
    .password-container {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .header-container {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .tip-box {
        background-color: #e6f3ff;
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #0066cc;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# ... keep analyze_password_strength function unchanged ...

def main():
    # Header with gradient background
    st.markdown("""
        <div class="header-container">
            <h1>🔒 Professional Password Strength Analyzer</h1>
            <p>Check how strong and secure your password is</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Create three columns for better layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="password-container">', unsafe_allow_html=True)
        
        # Password input with visibility toggle
        col_pass, col_toggle = st.columns([4, 1])
        with col_pass:
            password = st.text_input(
                "Enter your password:",
                type="password" if not st.session_state.get('password_visible', False) else "text",
                help="Enter the password you want to analyze"
            )
        with col_toggle:
            st.write("")
            st.write("")
            if st.checkbox("Show", key="password_visible"):
                st.session_state.password_visible = True
            else:
                st.session_state.password_visible = False
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if password:
            score, feedback, details = analyze_password_strength(password)
            
            # Enhanced score display
            st.markdown(f"""
                <div style='text-align: center; padding: 1rem;'>
                    <h2>Password Strength: {int(score)}%</h2>
                </div>
            """, unsafe_allow_html=True)
            st.progress(score/100)
            
            # Enhanced strength level display
            if score >= 80:
                st.success("🔒 VERY STRONG - Your password is excellent!")
            elif score >= 60:
                st.info("🔐 STRONG - Your password is good but can be improved")
            elif score >= 40:
                st.warning("⚠️ MODERATE - Your password needs improvement")
            else:
                st.error("⛔ WEAK - Your password is vulnerable to attacks")
            
            # Analysis in tabs
            tab1, tab2 = st.tabs(["📊 Detailed Analysis", "💡 Improvement Tips"])
            
            with tab1:
                for key, value in details.items():
                    st.markdown(f"""
                        <div class="tip-box">
                            <strong>{key}:</strong> {value}
                        </div>
                    """, unsafe_allow_html=True)
            
            with tab2:
                if feedback:
                    for suggestion in feedback:
                        st.warning(suggestion)
            
            # Enhanced security tips
            with st.expander("🛡️ Advanced Security Tips", expanded=False):
                st.markdown("""
                <div class="tip-box">
                    <h4>Best Practices for Strong Passwords:</h4>
                    <ul>
                        <li>🔄 Use unique passwords for each account</li>
                        <li>🔡 Mix uppercase, lowercase, numbers, and symbols</li>
                        <li>❌ Avoid using personal information</li>
                        <li>📏 Make it at least 12 characters long</li>
                        <li>🔐 Consider using a password manager</li>
                        <li>📱 Enable two-factor authentication when available</li>
                        <li>🚫 Avoid common word patterns and sequences</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()