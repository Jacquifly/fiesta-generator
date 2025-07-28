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

# --- Setup session state ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "just_logged_in" not in st.session_state:
    st.session_state.just_logged_in = False

# Login screen if not logged in
if not st.session_state.logged_in:
    st.title("🔐 Login Required")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        if username in st.secrets["users"] and st.secrets["users"][username] == password:
            st.session_state.logged_in = True
            st.session_state.just_logged_in = True
            st.session_state.username = username
            st.toast("🎉 Login successful!")
        else:
            st.error("Invalid username or password.")

    st.stop()  # 🔐 HARD stop so nothing else runs

# --- Splash after login
if st.session_state.just_logged_in:
    splash = st.empty()

    splash.markdown(
        f"""
        <div class="fade-out">
            <h2 style='text-align:center; color:#A98BFF;'>✨ Welcome, {st.session_state.username}! ✨</h2>
            <p style='text-align:center; color:#888;'>Loading your dashboard... please hold your pixels 🪄</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.spinner("Warming up the code cauldron..."):
        time.sleep(2)

    splash.empty()
    st.session_state.just_logged_in = False
    
# --- APP STARTS HERE
if st.session_state.logged_in:
# -- SIDEBAR USER MENU --
with st.sidebar:
    st.markdown("### 👤 User Menu")
    st.markdown(f"Logged in as: `{st.session_state.username}`")
    
    if st.button("🚪 Log Out"):
        # Reset all login/session flags
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.just_logged_in = False
        st.toast("🧼 You've been logged out.")

        # ❌ Don't render any more of the app
        st.stop()

    # -- TOP USER BANNER --
    st.markdown(
        f"""
        <div style='text-align: right; font-size: 14px; color: #aaa; padding-bottom: 0.5rem;'>
            Logged in as: <strong style='color: #f5f5f5;'>{st.session_state.username}</strong>
        </div>
        """,
        unsafe_allow_html=True
    )

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
