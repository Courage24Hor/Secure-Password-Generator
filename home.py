import streamlit as st
import secrets
import string
import pyperclip
import math

# ------------------ Password Logic ------------------ #
def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    pools = []
    characters = ""

    if use_upper:
        pools.append(string.ascii_uppercase)
        characters += string.ascii_uppercase
    if use_lower:
        pools.append(string.ascii_lowercase)
        characters += string.ascii_lowercase
    if use_digits:
        pools.append(string.digits)
        characters += string.digits
    if use_symbols:
        pools.append(string.punctuation)
        characters += string.punctuation

    if not characters:
        return ""

    # Ensure at least one char from each selected pool
    password = [secrets.choice(pool) for pool in pools]
    password += [secrets.choice(characters) for _ in range(length - len(password))]
    secrets.SystemRandom().shuffle(password)

    return "".join(password)


def password_strength(password):
    length = len(password)
    variety = len(set(password))
    entropy = length * math.log2(variety) if variety > 1 else 0

    if entropy < 40:
        return "Weak", "🔴"
    elif entropy < 60:
        return "Moderate", "🟠"
    elif entropy < 80:
        return "Strong", "🟢"
    else:
        return "Very Strong", "🔵"


# ------------------ Streamlit UI ------------------ #
st.set_page_config(
    page_title="Secure Password Generator",
    page_icon="🔐",
    layout="centered"
)

st.title("🔐 Secure Password Generator")
st.caption("Generate, evaluate, and manage strong passwords.")

with st.sidebar:
    st.header("⚙️ Settings")
    length = st.slider("Password Length", 8, 64, 16)
    use_upper = st.checkbox("Uppercase (A-Z)", True)
    use_lower = st.checkbox("Lowercase (a-z)", True)
    use_digits = st.checkbox("Numbers (0-9)", True)
    use_symbols = st.checkbox("Symbols (!@#$%)", True)

if "history" not in st.session_state:
    st.session_state.history = []

if st.button("Generate Password"):
    password = generate_password(
        length,
        use_upper,
        use_lower,
        use_digits,
        use_symbols
    )

    if password:
        st.session_state.history.insert(0, password)

        strength, icon = password_strength(password)

        st.subheader("Generated Password")
        st.code(password, language="text")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Strength", f"{icon} {strength}")
        with col2:
            if st.button("📋 Copy to Clipboard"):
                pyperclip.copy(password)
                st.success("Password copied!")

    else:
        st.error("Select at least one character type.")

if st.session_state.history:
    st.subheader("🕘 Password History")
    for i, p in enumerate(st.session_state.history[:5], start=1):
        st.code(f"{i}. {p}", language="text")
