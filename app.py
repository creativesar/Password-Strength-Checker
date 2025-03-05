import streamlit as st
import re
import math
import time

# Page configuration
st.set_page_config(
    page_title="Next-Gen Password Analyzer",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ultra Modern CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
        background: linear-gradient(135deg, #f6f8fd 0%, #f1f4f9 100%);
    }
    
    .stTextInput > div > div > input {
        font-size: 20px;
        padding: 20px;
        border-radius: 20px;
        border: 2px solid rgba(46, 134, 193, 0.1);
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #2E86C1;
        box-shadow: 0 0 25px rgba(46, 134, 193, 0.2);
        transform: translateY(-2px);
    }
    
    .requirement-item {
        padding: 12px 20px;
        margin: 8px 0;
        border-radius: 15px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .requirement-item:hover {
        transform: translateX(5px);
    }
    
    .requirement-item.met {
        color: #10B981;
        background: rgba(16, 185, 129, 0.1);
        border-left: 4px solid #10B981;
    }
    
    .requirement-item.unmet {
        color: #EF4444;
        background: rgba(239, 68, 68, 0.1);
        border-left: 4px solid #EF4444;
    }
    
    .strength-meter {
        padding: 30px;
        border-radius: 25px;
        margin: 25px 0;
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .strength-meter:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
    }
    
    .analysis-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        padding: 30px;
        border-radius: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        margin-bottom: 25px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .analysis-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
    }
    
    .stProgress > div > div > div > div {
        height: 15px;
        border-radius: 15px;
        background: linear-gradient(90deg, rgba(46, 134, 193, 0.2), rgba(46, 134, 193, 0.1));
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stProgress {
        backdrop-filter: blur(10px);
    }
    
    .stAlert {
        border-radius: 20px;
        border: none;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
        backdrop-filter: blur(10px);
    }
    
    .main {
        background: linear-gradient(135deg, #f6f8fd 0%, #f1f4f9 100%);
    }
    
    .css-1y4p8pa {
        padding: 3rem 5rem;
    }
    
    .metric-container {
        background: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
        margin: 15px 0;
        transition: all 0.4s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    }
    
    .password-requirements {
        background: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 20px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
    }
    
    .requirement-list {
        list-style-type: none;
        padding: 0;
    }
    
    .requirement-list li {
        padding: 8px 0;
        color: #666;
        transition: all 0.3s ease;
    }
    
    .requirement-list li:hover {
        color: #2E86C1;
        transform: translateX(5px);
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
    
    score += sum([
        2 if len(password) >= 12 else 1 if len(password) >= 8 else 0,
        1 if char_sets['uppercase'] else 0,
        1 if char_sets['lowercase'] else 0,
        1 if char_sets['numbers'] else 0,
        1 if char_sets['symbols'] else 0
    ])
    
    patterns = {
        r'(.)\1\1': "Repeated characters detected",
        r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)': "Sequential letters detected",
        r'(123|234|345|456|567|678|789|890)': "Sequential numbers detected"
    }
    
    for pattern, message in patterns.items():
        if re.search(pattern, password.lower()):
            score -= 1
            feedback.append(f"⚠️ {message}")
    
    if entropy > 80:
        score += 2
    elif entropy > 60:
        score += 1
    
    score = max(0, min(score, 4))
    
    return score, feedback, requirements, entropy

# Modern Header with 3D effect
st.markdown("""
    <div style='text-align: center; padding: 3rem 0;'>
        <h1 style='
            font-size: 3.5em;
            font-weight: 700;
            margin-bottom: 0.5rem;
            background: linear-gradient(120deg, #2E86C1, #3498DB, #21618C);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        '>🔐 Password Security Vault</h1>
        <p style='
            font-size: 1.4em;
            color: #666;
            margin-top: 1rem;
            font-weight: 400;
        '>Next-Generation Password Strength Analysis</p>
    </div>
""", unsafe_allow_html=True)

# Password requirements display
st.markdown("""
    <div class='password-requirements'>
        <h4 style='color: #2E86C1; margin-bottom: 15px;'>Password Requirements:</h4>
        <ul class='requirement-list'>
            <li>• Minimum 8 characters (12+ recommended)</li>
            <li>• At least one uppercase letter (A-Z)</li>
            <li>• At least one lowercase letter (a-z)</li>
            <li>• At least one number (0-9)</li>
            <li>• At least one special character (!@#$%^&*)</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

# Main content with glass morphism
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    password = st.text_input("Enter your password", type="password", key="password")

if 'password' in st.session_state:
    current_password = st.session_state.password
    if current_password:
        score, feedback, requirements, entropy = analyze_password(current_password)
        
        strength_colors = ['#EF4444', '#F59E0B', '#10B981', '#3B82F6', '#6366F1']
        strength_labels = ['Critical', 'Weak', 'Moderate', 'Strong', 'Fortress']
        strength_emojis = ['🚨', '⚠️', '⚡', '💪', '🔐']
        
        st.markdown(f"""
            <div class='strength-meter' style='background: linear-gradient(135deg, {strength_colors[score]}15, rgba(255,255,255,0.9));'>
                <h2 style='
                    text-align: center;
                    color: {strength_colors[score]};
                    margin: 0;
                    font-size: 2.2em;
                    font-weight: 600;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
                '>
                    {strength_emojis[score]} {strength_labels[score]}
                </h2>
            </div>
        """, unsafe_allow_html=True)
        
        progress_bar = st.progress(0)
        progress_bar.progress((score + 1) * 20)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                <div class='analysis-card'>
                    <h3 style='color: #2E86C1; margin-bottom: 20px; font-weight: 600;'>
                        Security Checklist
                    </h3>
                </div>
            """, unsafe_allow_html=True)
            
            for req, met in requirements.items():
                status = "met" if met else "unmet"
                icon = "✨" if met else "✖️"
                st.markdown(f"""
                    <div class='requirement-item {status}'>
                        {icon} {req}
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("""<div class='metric-container'>""", unsafe_allow_html=True)
            st.metric("🎯 Security Score", f"{entropy:.1f} bits", 
                     delta="Elite" if entropy > 60 else "Needs Enhancement")
            st.markdown("""</div>""", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class='analysis-card'>
                    <h3 style='color: #2E86C1; margin-bottom: 20px; font-weight: 600;'>
                        Smart Recommendations
                    </h3>
                </div>
            """, unsafe_allow_html=True)
            
            if feedback:
                for suggestion in feedback:
                    st.warning(suggestion)
            else:
                st.success("🌟 Outstanding! Your password is a security masterpiece!")
            
            if entropy < 50:
                st.info("💡 Pro Tip: Create an unbreakable password by combining unique characters")

# Modern footer with gradient
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 1.5rem;'>
        <p style='
            color: #666;
            font-size: 1.1em;
            background: linear-gradient(120deg, #2E86C1, #3498DB);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 500;
        '>
            Crafted with 🛡️ for next-level security
        </p>
    </div>
""", unsafe_allow_html=True)