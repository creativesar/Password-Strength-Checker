import streamlit as st
import re
import math

# Page configuration
st.set_page_config(
    page_title="Quantum Password Analyzer",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern Cyberpunk CSS with Real-Time Feedback
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto+Mono&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Roboto Mono', monospace;
        background: linear-gradient(135deg, #0F2027, #203A43, #2C5364);
        color: #E0E0E0;
    }
    
    .stTextInput > div > div > input {
        font-size: 1.2rem;
        padding: 1rem;
        border-radius: 25px;
        border: 2px solid #00D4FF;
        background: rgba(15, 32, 39, 0.9);
        color: #00D4FF;
        transition: all 0.4s ease;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.3);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #FF00FF;
        box-shadow: 0 0 25px rgba(255, 0, 255, 0.5);
        transform: scale(1.02);
    }
    
    .cyber-container {
        background: rgba(15, 32, 39, 0.85);
        border-radius: 25px;
        padding: 2rem;
        box-shadow: 0 0 40px rgba(0, 212, 255, 0.2);
        border: 1px solid rgba(0, 212, 255, 0.3);
        animation: pulse 2s infinite;
    }
    
    .strength-feedback {
        text-align: center;
        font-size: 1.5rem;
        margin-top: 1rem;
        font-family: 'Orbitron', sans-serif;
        text-shadow: 0 0 15px rgba(0, 212, 255, 0.5);
    }
    
    .char-indicator {
        display: inline-block;
        padding: 8px 15px;
        margin: 5px;
        border-radius: 15px;
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }
    
    .active {
        background: #00FF9F;
        color: #0F2027;
        box-shadow: 0 0 15px rgba(0, 255, 159, 0.5);
    }
    
    .inactive {
        background: rgba(44, 83, 100, 0.5);
        color: #666;
    }
    
    .requirement-item {
        padding: 10px;
        margin: 8px 0;
        border-radius: 10px;
        transition: all 0.4s ease;
        background: rgba(44, 83, 100, 0.5);
    }
    
    .requirement-item.met {
        color: #00FF9F;
        box-shadow: 0 0 15px rgba(0, 255, 159, 0.4);
        transform: translateX(5px);
    }
    
    .requirement-item.unmet {
        color: #FF3366;
        box-shadow: 0 0 15px rgba(255, 51, 102, 0.2);
    }
    
    .strength-meter {
        padding: 2rem;
        border-radius: 25px;
        margin: 1.5rem 0;
        background: linear-gradient(45deg, rgba(15, 32, 39, 0.9), rgba(44, 83, 100, 0.7));
        box-shadow: 0 0 30px rgba(0, 212, 255, 0.3);
    }
    
    .stProgress > div > div > div > div {
        height: 15px;
        border-radius: 15px;
        background: linear-gradient(90deg, #FF00FF, #00D4FF);
        box-shadow: 0 0 20px rgba(255, 0, 255, 0.5);
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 20px rgba(0, 212, 255, 0.2); }
        50% { box-shadow: 0 0 40px rgba(0, 212, 255, 0.4); }
        100% { box-shadow: 0 0 20px rgba(0, 212, 255, 0.2); }
    }
    
    .neon-text {
        animation: neon 1.5s ease-in-out infinite alternate;
    }
    
    @keyframes neon {
        from { text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #00D4FF; }
        to { text-shadow: 0 0 20px #fff, 0 0 30px #FF00FF, 0 0 40px #FF00FF; }
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
    pool_size = sum([26 if char_sets['lowercase'] else 0, 26 if char_sets['uppercase'] else 0,
                    10 if char_sets['numbers'] else 0, 32 if char_sets['symbols'] else 0])
    entropy = len(password) * math.log2(pool_size) if pool_size > 0 else 0
    return entropy, char_sets

def analyze_password(password):
    score = 0
    feedback = []
    entropy, char_sets = calculate_entropy(password)
    
    requirements = {
        "Length ≥ 8": len(password) >= 8,
        "Length ≥ 12": len(password) >= 12,
        "Uppercase": char_sets['uppercase'],
        "Lowercase": char_sets['lowercase'],
        "Numbers": char_sets['numbers'],
        "Symbols": char_sets['symbols']
    }
    
    score += sum([3 if len(password) >= 12 else 1 if len(password) >= 8 else 0,
                 2 if char_sets['uppercase'] else 0, 2 if char_sets['lowercase'] else 0,
                 2 if char_sets['numbers'] else 0, 2 if char_sets['symbols'] else 0])
    
    patterns = {r'(.)\1\1': "Repetition Alert", 
                r'(abc|bcd|...|xyz)': "Sequence Detected",
                r'(123|234|...|890)': "Numeric Pattern"}
    
    for pattern, message in patterns.items():
        if re.search(pattern, password.lower()):
            score -= 2
            feedback.append(f"⚠️ {message}")
    
    if entropy > 100: score += 3
    elif entropy > 80: score += 2
    elif entropy > 60: score += 1
    
    score = max(0, min(score, 5))
    return score, feedback, requirements, entropy, char_sets

# Cyberpunk Header
st.markdown("""
    <div style='text-align: center; padding: 3rem 0;'>
        <h1 class='neon-text' style='font-family: Orbitron, sans-serif; font-size: 3.5rem;'>
            🔐 Quantum Password Analyzer
        </h1>
        <p style='font-size: 1.2rem; color: #00D4FF; text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);'>
            Real-Time Security Matrix
        </p>
    </div>
""", unsafe_allow_html=True)

# Main content
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    password = st.text_input("Enter Encryption Key", type="password", key="password")
    
    # Real-Time Character Indicators (Top)
    if 'password' in st.session_state and st.session_state.password:
        current_password = st.session_state.password
        _, _, _, _, char_sets = analyze_password(current_password)
        
        st.markdown("<div style='text-align: center; margin-bottom: 1rem;'>", unsafe_allow_html=True)
        for char_type, active in char_sets.items():
            status = "active" if active else "inactive"
            st.markdown(f"<span class='char-indicator {status}'>{char_type.capitalize()}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Real-Time Strength Feedback (Below Input)
        score, _, _, _, _ = analyze_password(current_password)
        strength_data = [
            ("Critical", "#FF3366", "🚨"),
            ("Low", "#FF6699", "⚠️"),
            ("Medium", "#FFCC00", "🛡️"),
            ("High", "#00D4FF", "🔒"),
            ("Quantum", "#00FF9F", "🌌")
        ]
        st.markdown(f"""
            <div class='strength-feedback' style='color: {strength_data[score-1][1]};'>
                {strength_data[score-1][2]} {strength_data[score-1][0]}
            </div>
        """, unsafe_allow_html=True)
    
    # Detailed Analysis (Only shows if password exists)
    if 'password' in st.session_state and st.session_state.password:
        score, feedback, requirements, entropy, _ = analyze_password(current_password)
        
        # Strength Meter
        st.markdown(f"""
            <div class='strength-meter' style='border: 2px solid {strength_data[score-1][1]};'>
                <h2 style='text-align: center; color: {strength_data[score-1][1]}; font-family: Orbitron;'>
                    {strength_data[score-1][2]} {strength_data[score-1][0]} Security
                </h2>
            </div>
        """, unsafe_allow_html=True)
        
        progress_bar = st.progress(0)
        progress_bar.progress(score * 20)
        
        # Analysis Dashboard
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='cyber-container'><h3 style='color: #00D4FF;'>Security Matrix</h3></div>", unsafe_allow_html=True)
            for req, met in requirements.items():
                status = "met" if met else "unmet"
                icon = "✅" if met else "❌"
                st.markdown(f"<div class='requirement-item {status}'>{icon} {req}</div>", unsafe_allow_html=True)
            
            st.metric("🔋 Entropy Matrix", f"{entropy:.1f} bits",
                     delta="Quantum" if entropy > 80 else "Boost Needed",
                     delta_color="normal" if entropy > 80 else "inverse")
        
        with col2:
            st.markdown("<div class='cyber-container'><h3 style='color: #00D4FF;'>System Diagnostics</h3></div>", unsafe_allow_html=True)
            if feedback:
                for suggestion in feedback:
                    st.markdown(f"<div style='color: #FF3366; padding: 10px;'>{suggestion}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='color: #00FF9F; padding: 10px;'>✅ Optimal Security Configuration!</div>", unsafe_allow_html=True)
            
            if entropy < 60:
                st.markdown("<div style='color: #FFCC00; padding: 10px;'>💾 Upgrade Tip: Enhance complexity!</div>", unsafe_allow_html=True)

# Cyber Footer
st.markdown("""
    <div style='text-align: center; padding: 2rem; color: #00D4FF; text-shadow: 0 0 15px rgba(0, 212, 255, 0.5);'>
        <p>Powered by xAI Quantum Systems | © 2025</p>
    </div>
""", unsafe_allow_html=True)