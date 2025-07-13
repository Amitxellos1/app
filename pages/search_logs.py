import streamlit as st
from utils.db import fetch_logs

def show():
    st.title("Search Logs")
    q = st.text_input("Search term")
    category = st.selectbox("Category", ["", "UI", "Backend", "Network", "Database"])
    if st.button("Search"):
        rows = fetch_logs(q, category)
        st.dataframe(rows)
