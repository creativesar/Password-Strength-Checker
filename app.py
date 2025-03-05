import streamlit as st
import re
import math

# Page configuration
st.set_page_config(
    page_title="Password Strength Analyzer",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    .stTextInput > div > div > input {
        font-size: 18px;
        padding: 15px;
        border-radius: 15px;
        border: 2px solid #eee;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #2E86C1;
        box-shadow: 0 0 15px rgba(46, 134, 193, 0.2);
    }
    
    .requirement-item {
        padding: 8px;
        margin: 5px 0;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .requirement-item.met {
        color: #228B22;
        background-color: #f0fff0;
    }
    
    .requirement-item.unmet {
        color: #DC143C;
        background-color: #fff0f0;
    }
    
    .strength-meter {
        padding: 25px;
        border-radius: 20px;
        margin: 20px 0;
        background: #fff;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .analysis-card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    .stProgress > div > div > div > div {
        height: 12px;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

def calculate_entropy(password):
    char_sets = {
        'lowercase': len(re.findall(r'[a-z]', password)) > 0,
        'uppercase': len(re.findall(r'[A-Z]', password)) > 0,
        'numbers': len(re.findall(r'[0-9]', password)) > 0,
        'symbols': len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', password)) > 0
    }
    
    pool_size = sum([
        26 if char_sets['lowercase'] else 0,
        26 if char_sets['uppercase'] else 0,
        10 if char_sets['numbers'] else 0,
        32 if char_sets['symbols'] else 0
    ])
    
    entropy = len(password) * math.log2(pool_size) if pool_size > 0 else 0
    return entropy, char_sets

def analyze_password(password):
    score = 0
    feedback = []
    entropy, char_sets = calculate_entropy(password)
    
    requirements = {
        "Length ≥ 8 characters": len(password) >= 8,
        "Length ≥ 12 characters": len(password) >= 12,
        "Uppercase letters": char_sets['uppercase'],
        "Lowercase letters": char_sets['lowercase'],
        "Numbers": char_sets['numbers'],
        "Special characters": char_sets['symbols']
    }
    
    # Scoring
    score += sum([
        2 if len(password) >= 12 else 1 if len(password) >= 8 else 0,
        1 if char_sets['uppercase'] else 0,
        1 if char_sets['lowercase'] else 0,
        1 if char_sets['numbers'] else 0,
        1 if char_sets['symbols'] else 0
    ])
    
    # Pattern checks
    patterns = {
        r'(.)\1\1': "Repeated characters detected",
        r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)': "Sequential letters detected",
        r'(123|234|345|456|567|678|789|890)': "Sequential numbers detected"
    }
    
    for pattern, message in patterns.items():
        if re.search(pattern, password.lower()):
            score -= 1
            feedback.append(f"⚠️ {message}")
    
    # Entropy bonus
    if entropy > 80:
        score += 2
    elif entropy > 60:
        score += 1
    
    score = max(0, min(score, 4))
    
    return score, feedback, requirements, entropy

# Modern Header
st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='
            font-size: 3em;
            font-weight: 700;
            margin-bottom: 0.5rem;
            background: linear-gradient(120deg, #2E86C1, #3498DB, #21618C);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        '>🛡️ Password Security Analyzer</h1>
        <p style='
            font-size: 1.3em;
            color: #666;
            margin-top: 0.5rem;
            font-weight: 300;
        '>Real-time password strength evaluation</p>
    </div>
""", unsafe_allow_html=True)

# Main content
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    password = st.text_input("Enter your password", type="password", key="password")

if 'password' in st.session_state:
    current_password = st.session_state.password
    if current_password:
        score, feedback, requirements, entropy = analyze_password(current_password)
        
        # Strength visualization
        strength_colors = ['#DC143C', '#FF4500', '#FFA500', '#9ACD32', '#228B22']
        strength_labels = ['Very Weak', 'Weak', 'Medium', 'Strong', 'Very Strong']
        strength_emojis = ['⚠️', '❗', '⚡', '💪', '🔒']
        
        # Progress and strength indicator
        st.markdown(f"""
            <div class='strength-meter' style='background: linear-gradient(135deg, {strength_colors[score]}15, white);'>
                <h2 style='text-align: center; color: {strength_colors[score]}; margin: 0;'>
                    {strength_emojis[score]} {strength_labels[score]}
                </h2>
            </div>
        """, unsafe_allow_html=True)
        
        progress_bar = st.progress(0)
        progress_bar.progress((score + 1) * 20)
        
        # Requirements and Analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                <div class='analysis-card'>
                    <h3 style='color: #2E86C1; margin-bottom: 20px;'>Password Requirements</h3>
                </div>
            """, unsafe_allow_html=True)
            
            for req, met in requirements.items():
                status = "met" if met else "unmet"
                icon = "✅" if met else "❌"
                st.markdown(f"""
                    <div class='requirement-item {status}'>
                        {icon} {req}
                    </div>
                """, unsafe_allow_html=True)
            
            st.metric("🎯 Entropy Score", f"{entropy:.1f} bits", 
                     delta="Strong" if entropy > 60 else "Needs improvement")
        
        with col2:
            st.markdown("""
                <div class='analysis-card'>
                    <h3 style='color: #2E86C1; margin-bottom: 20px;'>Suggestions</h3>
                </div>
            """, unsafe_allow_html=True)
            
            if feedback:
                for suggestion in feedback:
                    st.warning(suggestion)
            else:
                st.success("🎉 Excellent! Your password meets all security criteria!")
            
            if entropy < 50:
                st.info("💡 Pro Tip: Mix different types of characters and increase length")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 1rem;'>
        <p style='color: #666;'>
            Built with 🛡️ for enhanced security
        </p>
    </div>
""", unsafe_allow_html=True)