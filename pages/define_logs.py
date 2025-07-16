import streamlit as st
from utils.db import insert_log

SECTION_FIELDS = {
    "General Information": ["description", "reference", "dev", "qe", "data", "property_key"],
    "Event Details": [
        "guid", "coll_dts", "context_guid", "context_sequence", "dts_start", "dts_end",
        "workflow", "category", "subcategory", "type", "subtype", "user_guid", "offline",
        "ip", "user_agent", "language", "device_guid", "session_guid", "error_code",
        "error_type", "error_desc", "cloud_id", "count", "value", "pagename", "mcid_guid",
        "build", "url", "referrer", "idp", "org_guid", "connection"
    ],
    "Source Information": ["client_id", "name", "version", "platform", "device", "os_version", "app_store_id"],
    "Content Details": ["id", "name", "type", "size", "extension", "mimetype", "category", "status", "action", "author"],
    "UI Details": ["view_type", "search_keyword", "filter", "sort_order", "sequence"],
    "Environment Details": [
        "fw_name", "fw_version", "com_name", "com_version", "svc_name", "svc_version", "api_name", "api_version"
    ],
    "Consumer Information": ["client_id", "name", "version", "platform", "device", "os_version", "app_store_id"],
    "User Subscription Details": ["service_code", "service_level"],
    "Transaction Details": ["number", "product", "quantity", "amount"],
    "Experimentation Details": [
        "request_guid", "response_guid", "surface_id", "campaign_id", "variation_id",
        "action_block_id", "container_id", "treatment_id", "control_group_id", "experience_id"
    ],
    "Context": ["guid", "init", "params"],
    "Entity Information": ["ims", "ngl", "device", "env", "source", "event"],
    "Custom Information": ["params", "content_params", "feedback_comments"]
}

def show():
    st.title("📝 Define Log Event with Field Selector")

    st.info("👈 Select sections and fields you want to fill.")

    # Select Sections
    selected_sections = st.multiselect("Select Sections", list(SECTION_FIELDS.keys()))

    field_inputs = {}

    with st.form("define_log_form"):
        st.subheader("Selected Fields")

        for section in selected_sections:
            st.markdown(f"### 🔹 {section}")
            selected_fields = st.multiselect(f"Fields in {section}", SECTION_FIELDS[section], key=f"{section}_fields")

            # Render input fields for selected
            for field in selected_fields:
                full_key = f"{section}_{field}".replace(" ", "_").lower()
                field_inputs[full_key] = st.text_input(f"{section} → {field}")

        created_by = st.text_input("Created By", value="PM/DS Name")

        submitted = st.form_submit_button("Submit Log Event")

    if submitted:
        # Flatten dictionary for submission
        event_data = {k: v for k, v in field_inputs.items()}
        event_data["created_by"] = created_by

        insert_log(event_data, created_by=created_by)
        st.success("✅ Log event saved successfully!")

