import streamlit as st
from utils.db import insert_log

def show_define_logs():
    st.title("📝 Define New Log Event")

    with st.form("define_log_form"):
        st.subheader("Basic Info")
        col1, col2, col3 = st.columns(3)

        when = col1.date_input("When")
        description = st.text_area("Description")
        reference = st.text_input("Reference (if any)")

        dev = col1.text_input("Dev")
        qe = col2.text_input("QE")
        data = col3.text_input("Data")
        property_key = st.text_input("Property Key")

        st.subheader("Event Metadata")
        event_workflow = st.text_input("Event Workflow")
        event_category = st.text_input("Event Category")
        event_type = st.text_input("Event Type")
        event_subtype = st.text_input("Event Subtype")

        st.subheader("Source Info")
        source_name = st.text_input("Source Name")
        source_version = st.text_input("Source Version")

        st.subheader("Creator Info")
        created_by = st.text_input("Created By", value="PM/DS Name")

        submitted = st.form_submit_button("Submit Log Event")

    if submitted:
        # Prepare data dict matching your SQLite schema
        event_data = {
            "when": str(when),
            "description": description,
            "reference": reference,
            "dev": dev,
            "qe": qe,
            "data": data,
            "property_key": property_key,
            "event_workflow": event_workflow,
            "event_category": event_category,
            "event_type": event_type,
            "event_subtype": event_subtype,
            "source_name": source_name,
            "source_version": source_version,
            "created_by": created_by
        }

        insert_log(event_data, created_by=created_by)
        st.success("✅ Log event saved successfully!")
