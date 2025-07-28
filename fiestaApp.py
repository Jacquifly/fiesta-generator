import random
import string
import pandas as pd
import streamlit as st
import time

# Read credentials from secrets.toml
USER_CREDENTIALS = st.secrets["users"]

#  Login block
import streamlit as st
import time

# --- Session state setup ---
# --- Initialize session state ---
# --- Session state setup ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "just_logged_in" not in st.session_state:
    st.session_state.just_logged_in = False

# --- LOGIN FORM ---
if not st.session_state.logged_in:
    st.title("🔐 Login Required")

    # ✅ Login form captures Enter key AND button clicks
    with st.form("login_form"):
        st.text_input("Username", key="login_username")
        st.text_input("Password", type="password", key="login_password")
        login_submitted = st.form_submit_button("Login")

    if login_submitted:
        username = st.session_state.login_username
        password = st.session_state.login_password

        if username in st.secrets["users"] and st.secrets["users"][username] == password:
            st.session_state.logged_in = True
            st.session_state.just_logged_in = True
            st.session_state.username = username
            st.toast("🎉 Login successful!")
            st.stop()
        else:
            st.error("Invalid username or password.")

    # Stop app if still on login screen
    st.stop()

# --- TRANSITION SPLASH (shown only immediately after login) ---
if st.session_state.just_logged_in:
    splash_placeholder = st.empty()  # 🔮 Temporary zone for the splash

    # Fill it with the splash message
    splash_placeholder.markdown(
        """
        <style>
        .center-text {
            text-align: center;
            font-size: 28px;
            font-weight: bold;
            padding-top: 50px;
            color: #A98BFF;
        }
        .sub-text {
            text-align: center;
            font-size: 18px;
            color: #aaa;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    splash_placeholder.markdown(
        f'<div class="center-text">✨ Welcome, {st.session_state.username}! ✨</div>',
        unsafe_allow_html=True
    )
    splash_placeholder.markdown(
        '<div class="sub-text">Loading your dashboard... please hold your pixels 🪄</div>',
        unsafe_allow_html=True
    )

    # Spinner delay
    with st.spinner("Warming up your code cauldron..."):
        time.sleep(2)

    # 💥 Clear the splash after the delay
    splash_placeholder.empty()
    st.session_state.just_logged_in = False

#  Code Generator Page
st.set_page_config(page_title="Secure Code Generator", layout="centered")

st.title("🔐 16-Digit Code Generator")
st.markdown("Generate 16-digit numeric codes with a 6-letter alpha prefix.")

# 🔄 Session state to track if codes were generated
if "codes" not in st.session_state:
    st.session_state.codes = []
if "generated_once" not in st.session_state:
    st.session_state.generated_once = False

# Inputs
prefix = st.text_input("Enter a 6-letter prefix", max_chars=6).upper()
num_codes = st.number_input("Number of codes to generate", min_value=1, max_value=1000, value=300)

# Validate prefix
if len(prefix) != 6 or not prefix.isalpha():
    st.warning("Prefix must be exactly 6 letters (no numbers).")
    st.stop()

# 🔧 Function to generate codes
def generate_codes(prefix, num, length=10):
    codes = set()
    while len(codes) < num:
        numeric_part = ''.join(random.choices(string.digits, k=length))
        codes.add(f"{prefix}{numeric_part}")
    return list(codes)

# 📦 Code generation UI
col1, col2 = st.columns([1, 1])

# 🎯 Generate or Regenerate button
with col1:
    button_label = "🔁 Regenerate Codes" if st.session_state.generated_once else "🚀 Generate Codes"
    if st.button(button_label):
        st.session_state.codes = generate_codes(prefix, num_codes)
        st.session_state.generated_once = True
        st.toast("🎉 Codes generated successfully!")  # This is our confetti vibe!

# ❌ Clear button (only visible *after* generation)
with col2:
    if st.session_state.generated_once:
        if st.button("🧹 Clear Codes"):
            st.session_state.codes = []
            st.session_state.generated_once = False

# 🧾 Show DataFrame + Download if codes exist
if st.session_state.codes:
    df = pd.DataFrame(st.session_state.codes, columns=["Code"])
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"{prefix}_generated_codes.csv",
        mime='text/csv'
    )
