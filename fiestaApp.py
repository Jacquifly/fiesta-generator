import random
import string
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Code Generator", layout="centered")

st.title("🔐 16-Digit Code Generator")

# ✏️ Input for the prefix
prefix = st.text_input("Enter a 6-letter prefix for your codes", max_chars=6).upper()

# 🧮 Input for number of codes
num_codes = st.number_input("How many codes would you like to generate?", min_value=1, max_value=1000, value=300)

# Only show the button if a valid prefix is entered
if len(prefix) != 6 or not prefix.isalpha():
    st.warning("Please enter exactly **6 letters** as your prefix.")
    st.stop()

# ✅ Generate codes button
if st.button("🚀 Generate Codes"):

    def generate_codes(prefix, num, length=10):
        codes = set()
        while len(codes) < num:
            numeric_part = ''.join(random.choices(string.digits, k=length))
            codes.add(f"{prefix}{numeric_part}")
        return list(codes)

    codes = generate_codes(prefix, num_codes)

    df = pd.DataFrame(codes, columns=["Code"])
    st.success(f"🎉 Generated {len(codes)} codes with prefix: {prefix}")

    # Show preview
    st.dataframe(df)

    # 📥 Download button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"{prefix}_generated_codes.csv",
        mime='text/csv'
    )
