import random
import string
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Secure Code Generator", layout="centered")

st.title("🔐 16-Digit Code Generator")
st.markdown("Generate 16-digit numeric codes with a 6-letter alpha prefix.")

# Initialize session state
if "codes" not in st.session_state:
    st.session_state.codes = []

# Input prefix
prefix = st.text_input("Enter a 6-letter prefix", max_chars=6).upper()

# Input number of codes
num_codes = st.number_input("Number of codes to generate", min_value=1, max_value=1000, value=300)

# Validate prefix
if len(prefix) != 6 or not prefix.isalpha():
    st.warning("Prefix must be exactly 6 letters (no numbers).")
    st.stop()

# Buttons: Generate and Clear/Regenerate
col1, col2 = st.columns(2)
with col1:
    generate = st.button("🚀 Generate Codes")
with col2:
    clear_and_regenerate = st.button("🔄 Clear & Regenerate")

# Code generation function
def generate_codes(prefix, num, length=10):
    codes = set()
    while len(codes) < num:
        numeric_part = ''.join(random.choices(string.digits, k=length))
        codes.add(f"{prefix}{numeric_part}")
    return list(codes)

# Generate or regenerate codes
if generate or clear_and_regenerate:
    st.session_state.codes = generate_codes(prefix, num_codes)

# Display generated codes
if st.session_state.codes:
    df = pd.DataFrame(st.session_state.codes, columns=["Code"])
    st.dataframe(df)

    # CSV download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"{prefix}_generated_codes.csv",
        mime='text/csv'
    )
