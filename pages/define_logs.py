import streamlit as st
from utils.db import insert_log

def show():
    st.title("Define New Log Event")
    with st.form("log_form"):
        name = st.text_input("Event Name")
        description = st.text_area("Description")
        category = st.selectbox("Category", ["UI", "Backend", "Network", "Database"])
        module = st.text_input("Source Module")
        severity = st.selectbox("Severity", ["Info", "Warning", "Error", "Critical"])
        version = st.number_input("Version", min_value=1, step=1)
        created_by = st.text_input("Created By")
        submitted = st.form_submit_button("Submit")

    if submitted:
        insert_log(name, description, category, module, severity, version, created_by)
        st.success("Log event submitted successfully!")
