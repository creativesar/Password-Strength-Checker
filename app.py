import streamlit as st
import pandas as pd
import time

# Function to check password strength
def check_password_strength(password):
    strength = 0
    feedback = []

    # Check length (increased to 12)
    if len(password) >= 12:
        strength += 1
    else:
        feedback.append("Password should be at least 12 characters long.")

    # Check for uppercase letters (at least 2)
    uppercase_count = sum(1 for char in password if char.isupper())
    if uppercase_count >= 2:
        strength += 1
    else:
        feedback.append("Password should contain at least two uppercase letters.")

    # Check for lowercase letters
    if any(char.islower() for char in password):
        strength += 1
    else:
        feedback.append("Password should contain at least one lowercase letter.")

    # Check for numbers (at least 2)
    digit_count = sum(1 for char in password if char.isdigit())
    if digit_count >= 2:
        strength += 1
    else:
        feedback.append("Password should contain at least two numbers.")

    # Check for special characters (at least 2)
    special_chars = sum(1 for char in password if not char.isalnum())
    if special_chars >= 2:
        strength += 1
    else:
        feedback.append("Password should contain at least two special characters.")

    # Check for consecutive characters
    for i in range(len(password) - 2):
        if password[i] == password[i+1] == password[i+2]:
            feedback.append("Password shouldn't contain three consecutive identical characters.")
            strength -= 1
            break

    # Check for keyboard patterns
    keyboard_patterns = ['qwerty', 'asdfgh', '123456', 'zxcvbn']
    if any(pattern.lower() in password.lower() for pattern in keyboard_patterns):
        feedback.append("Password contains common keyboard patterns.")
        strength -= 1

    # Expanded common password check
    common_passwords = [
        "password", "123456", "qwerty", "admin", "letmein", "welcome",
        "monkey", "dragon", "baseball", "football", "master", "hello",
        "abc123", "123456789", "password1", "superman", "iloveyou"
    ]
    if password.lower() in common_passwords:
        feedback.append("Password is too common. Please choose a stronger password.")
        strength = 0

    # Determine strength level (adjusted scoring)
    if strength >= 5:
        return "Strong", feedback
    elif strength >= 3:
        return "Moderate", feedback
    else:
        return "Weak", feedback

# Streamlit app
def main():
    st.set_page_config(page_title="Password Strength Checker", page_icon="🔒", layout="centered")
    st.title("🔒 Password Strength Checker")
    st.write("Enter a password to check its strength and ensure it meets the requirements.")

    # Custom CSS for modern look
    st.markdown("""
        <style>
        .main {
            background-color: #f0f2f6;
        }
        .stTextInput > div > div > input {
            border-radius: 10px;
        }
        .stProgress > div > div > div > div {
            background-color: linear-gradient(to right, #ff4b4b, #7e56d9);
            border-radius: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Animated title
    st.markdown("""
        <h1 style='text-align: center; color: #7e56d9; animation: fadeIn 2s;'>
            🔒 Password Strength Checker
        </h1>
        <style>
        @keyframes fadeIn {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }
        </style>
    """, unsafe_allow_html=True)

    # Modern container for the main content
    with st.container():
        st.markdown("""
            <div style='background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
        """, unsafe_allow_html=True)
        
        # Password input with improved UI
        col1, col2 = st.columns([3, 1])
        with col1:
            password = st.text_input("🔑 Enter your password:", type="password", key="password_input")
        with col2:
            show_password = st.checkbox("👁️ Show")

        if show_password:
            st.text_input("", value=password, disabled=True, key="visible_password")

        # Animated strength indicator
        if password:
            strength, feedback = check_password_strength(password)
            
            # Animated progress bar
            progress_placeholder = st.empty()
            if strength == "Strong":
                color = "#00cc00"
                progress = 1.0
            elif strength == "Moderate":
                color = "#ffa500"
                progress = 0.66
            else:
                color = "#ff0000"
                progress = 0.33

            for i in range(0, 101, 10):
                time.sleep(0.05)
                progress_placeholder.progress(i/100)
            # Strength indicator with emoji and color
            st.markdown(f"""
                <h3 style='text-align: center; color: {color}; animation: bounce 1s;'>
                    {strength} {'💪' if strength == 'Strong' else '⚠️' if strength == 'Moderate' else '❌'}
                </h3>
                <style>
                @keyframes bounce {{
                    0%, 20%, 50%, 80%, 100% {{transform: translateY(0);}}
                    40% {{transform: translateY(-20px);}}
                    60% {{transform: translateY(-10px);}}
                }}
                </style>
            """, unsafe_allow_html=True)

        # Modern requirements display
        with st.expander("📋 Password Requirements", expanded=True):
            requirements = {
                "Minimum 12 characters": len(password) >= 12,
                "At least 2 uppercase letters": sum(1 for char in password if char.isupper()) >= 2,
                "At least 1 lowercase letter": any(char.islower() for char in password),
                "At least 2 numbers": sum(1 for char in password if char.isdigit()) >= 2,
                "At least 2 special characters": sum(1 for char in password if not char.isalnum()) >= 2,
                "No three consecutive identical characters": not any(password[i] == password[i+1] == password[i+2] for i in range(len(password) - 2)),
                "No common keyboard patterns": not any(pattern.lower() in password.lower() for pattern in ['qwerty', 'asdfgh', '123456', 'zxcvbn']),
                "Not a common password": password.lower() not in [
                    "password", "123456", "qwerty", "admin", "letmein", "welcome",
                    "monkey", "dragon", "baseball", "football", "master", "hello",
                    "abc123", "123456789", "password1", "superman", "iloveyou"
                ]
            }

            for requirement, met in requirements.items():
                st.markdown(f"- {'✅' if met else '❌'} {requirement}")

        # Feedback with animations
        if password and feedback:
            st.markdown("""
                <h4 style='color: #7e56d9; animation: slideIn 1s;'>
                    💡 Suggestions for Improvement
                </h4>
                <style>
                @keyframes slideIn {
                    0% { transform: translateX(-100%); }
                    100% { transform: translateX(0); }
                }
                </style>
            """, unsafe_allow_html=True)
            
            for item in feedback:
                st.error(item)

        # Modern logging display
        if password:
            with st.expander("📊 Password Analysis Log"):
                data = {
                    "Password": ["*" * len(password)],
                    "Strength": [strength],
                    "Feedback": [", ".join(feedback)]
                }
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True)

# Run the app
if __name__ == "__main__":
    main()