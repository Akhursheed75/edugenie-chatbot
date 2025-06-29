import streamlit as st

st.title("🧪 Streamlit Test App")

name = st.text_input("Aapka naam kya hai?")
if name:
    st.success(f"Welcome, {name}!")
