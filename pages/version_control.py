import streamlit as st
from utils.db import fetch_versions

def show():
    st.title("Version Control")
    event = st.text_input("Event Name")
    if st.button("Load Version History"):
        history = fetch_versions(event)
        st.table(history)
        clashes = history.duplicated(subset=['name', 'version']).any()
        if clashes:
            st.error("⚠️ Version conflicts detected!")
