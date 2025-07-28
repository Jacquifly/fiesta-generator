import random
import string
import pandas as pd
import streamlit as st

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
