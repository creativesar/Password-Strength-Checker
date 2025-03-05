import streamlit as st
import pandas as pd

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

    # Password input with visibility toggle
    col1, col2 = st.columns([3, 1])
    with col1:
        password = st.text_input("Enter your password:", type="password", key="password_input")
    with col2:
        show_password = st.checkbox("Show Password")

    if show_password:
        st.text_input("", value=password, disabled=True, key="visible_password")

    # Display password requirements
    st.subheader("Password Requirements")
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

    if password:
        # Check password strength
        strength, feedback = check_password_strength(password)

        # Display strength with a progress bar
        st.subheader("Password Strength:")
        if strength == "Strong":
            st.success("✅ Strong")
            st.progress(1.0)
        elif strength == "Moderate":
            st.warning("⚠️ Moderate")
            st.progress(0.66)
        else:
            st.error("❌ Weak")
            st.progress(0.33)

        # Display feedback
        if feedback:
            st.subheader("Feedback:")
            for item in feedback:
                st.write(f"- {item}")

        # Optional: Save results to a DataFrame (for logging or analysis)
        data = {
            "Password": [password],
            "Strength": [strength],
            "Feedback": [", ".join(feedback)]
        }
        df = pd.DataFrame(data)
        st.write("Log:")
        st.dataframe(df)

# Run the app
if __name__ == "__main__":
    main()