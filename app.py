import streamlit as st
import re
import math

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
    .strength-meter {
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

def calculate_entropy(password):
    # Calculate password entropy (randomness)
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
    return entropy

def analyze_password(password):
    score = 0
    feedback = []
    
    # Length check
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long")
    
    # Character variety checks
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Add uppercase letters")
    
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Add lowercase letters")
    
    if re.search(r'[0-9]', password):
        score += 1
    else:
        feedback.append("Add numbers")
    
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    else:
        feedback.append("Add special characters")
    
    # Pattern checks
    if re.search(r'(.)\1\1', password):
        score -= 1
        feedback.append("Avoid repeated characters")
    
    if re.search(r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', password.lower()):
        score -= 1
        feedback.append("Avoid sequential letters")
    
    if re.search(r'(123|234|345|456|567|678|789|890)', password):
        score -= 1
        feedback.append("Avoid sequential numbers")
    
    # Entropy bonus
    entropy = calculate_entropy(password)
    if entropy > 80:
        score += 2
    elif entropy > 60:
        score += 1
    
    # Normalize score
    score = max(0, min(score, 4))
    
    return score, feedback

# Header
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>🔒 Advanced Password Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2em;'>Check how strong your password is!</p>", unsafe_allow_html=True)

# Password input
password = st.text_input("Enter your password", type="password")

if password:
    score, feedback = analyze_password(password)
    
    # Strength visualization
    strength_colors = ['#DC143C', '#FF4500', '#FFA500', '#9ACD32', '#228B22']
    strength_labels = ['Very Weak', 'Weak', 'Medium', 'Strong', 'Very Strong']
    
    # Progress bar
    progress_bar = st.progress(0)
    progress_bar.progress((score + 1) * 20)
    
    # Strength label
    st.markdown(f"<h3 style='text-align: center; color: {strength_colors[score]};'>{strength_labels[score]}</h3>", unsafe_allow_html=True)
    
    # Password analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Password Analysis")
        entropy = calculate_entropy(password)
        st.metric("Entropy Score", f"{entropy:.1f} bits")
        
        checks = {
            "Length (≥ 8)": len(password) >= 8,
            "Length (≥ 12)": len(password) >= 12,
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
        if feedback:
            for suggestion in feedback:
                st.warning(suggestion)
        else:
            st.success("Excellent! Your password meets all security criteria!")
        
        if entropy < 50:
            st.info("💡 Tip: Consider using a longer password with more variety of characters")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>Made with ❤️ for security</p>", unsafe_allow_html=True)