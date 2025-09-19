import streamlit as st

if globals().get('page_title') is None:
    page_title = "👋 Hello from INFO-5940!"

st.set_page_config(page_title="Hello Codespaces", layout="centered")

st.title(page_title)

st.write("If you can see this page, Streamlit is running correctly inside your Codespace.")

name = st.text_input("What is your name?")
if name:
    st.success(f"Nice to meet you, {name}!")
    page_title = "We're one testin"

st.markdown("---")
st.caption("This is a test app for INFO 5940 Fall 2025.")