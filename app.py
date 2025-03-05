import streamlit as st
import pandas as pd

# Function to check password strength
def check_password_strength(password):
    strength = 0
    feedback = []

    # Check length
    if len(password) >= 8:
        strength += 1
    else:
        feedback.append("Password should be at least 8 characters long.")

    # Check for uppercase letters
    if any(char.isupper() for char in password):
        strength += 1
    else:
        feedback.append("Password should contain at least one uppercase letter.")

    # Check for lowercase letters
    if any(char.islower() for char in password):
        strength += 1
    else:
        feedback.append("Password should contain at least one lowercase letter.")

    # Check for numbers
    if any(char.isdigit() for char in password):
        strength += 1
    else:
        feedback.append("Password should contain at least one number.")

    # Check for special characters
    if any(not char.isalnum() for char in password):
        strength += 1
    else:
        feedback.append("Password should contain at least one special character.")

    # Common password check (you can expand this list)
    common_passwords = ["password", "123456", "qwerty", "admin", "letmein"]
    if password.lower() in common_passwords:
        feedback.append("Password is too common. Please choose a stronger password.")
        strength = 0

    # Determine strength level
    if strength == 5:
        return "Strong", feedback
    elif strength >= 3:
        return "Moderate", feedback
    else:
        return "Weak", feedback

# Streamlit app
def main():
    st.title("Password Strength Checker")
    st.write("Enter a password to check its strength.")

    # Input field for password
    password = st.text_input("Enter your password:", type="password")

    if password:
        # Check password strength
        strength, feedback = check_password_strength(password)

        # Display strength
        st.subheader("Password Strength:")
        if strength == "Strong":
            st.success("✅ Strong")
        elif strength == "Moderate":
            st.warning("⚠️ Moderate")
        else:
            st.error("❌ Weak")

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