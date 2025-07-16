import streamlit as st
from utils.db import insert_log
from datetime import datetime
import json

def show():
    st.title("📝 Define Full Log Event")
    
    # Add helpful description
    st.markdown("""
    Use this form to define a comprehensive log event with all relevant details.
    Fields marked with * are required.
    """)

    with st.form("define_full_log_form"):
        # General Information Section
        st.subheader("🔹 General Information")
        col1, col2 = st.columns(2)
        
        with col1:
            description = st.text_area("Description *", help="Brief description of the log event")
            reference = st.text_input("Reference", help="Reference number or ID if any")
            property_key = st.text_input("Property Key *", help="Unique identifier for this property")
        
        with col2:
            created_by = st.text_input("Created By *", value="PM/DS Name", help="Your name or ID")
            
        # Team Information
        st.write("**Team Information**")
        dev_col, qe_col, data_col = st.columns(3)
        with dev_col:
            dev = st.text_input("Dev Team")
        with qe_col:
            qe = st.text_input("QE Team")
        with data_col:
            data = st.text_input("Data Team")

        # Event Details Section
        st.subheader("🔹 Event Details")
        event_data = create_input_section("event", [
            ("guid", "Event GUID"),
            ("coll_dts", "Collection Timestamp"),
            ("context_guid", "Context GUID"),
            ("context_sequence", "Context Sequence"),
            ("dts_start", "Start Timestamp"),
            ("dts_end", "End Timestamp"),
            ("workflow", "Workflow"),
            ("category", "Category"),
            ("subcategory", "Subcategory"),
            ("type", "Type"),
            ("subtype", "Subtype"),
            ("user_guid", "User GUID"),
            ("offline", "Offline Status"),
            ("ip", "IP Address"),
            ("user_agent", "User Agent"),
            ("language", "Language"),
            ("device_guid", "Device GUID"),
            ("session_guid", "Session GUID"),
            ("error_code", "Error Code"),
            ("error_type", "Error Type"),
            ("error_desc", "Error Description"),
            ("cloud_id", "Cloud ID"),
            ("count", "Count"),
            ("value", "Value"),
            ("pagename", "Page Name"),
            ("mcid_guid", "MCID GUID"),
            ("build", "Build Version"),
            ("url", "URL"),
            ("referrer", "Referrer"),
            ("idp", "Identity Provider"),
            ("org_guid", "Organization GUID"),
            ("connection", "Connection Type")
        ])

        # Source Information Section
        st.subheader("🔹 Source Information")
        source_data = create_input_section("source", [
            ("client_id", "Client ID"),
            ("name", "Source Name"),
            ("version", "Version"),
            ("platform", "Platform"),
            ("device", "Device"),
            ("os_version", "OS Version"),
            ("app_store_id", "App Store ID")
        ])

        # Content Details Section
        st.subheader("🔹 Content Details")
        content_data = create_input_section("content", [
            ("id", "Content ID"),
            ("name", "Content Name"),
            ("type", "Content Type"),
            ("size", "Size"),
            ("extension", "File Extension"),
            ("mimetype", "MIME Type"),
            ("category", "Category"),
            ("status", "Status"),
            ("action", "Action"),
            ("author", "Author")
        ])

        # UI Details Section
        st.subheader("🔹 UI Details")
        ui_data = create_input_section("ui", [
            ("view_type", "View Type"),
            ("search_keyword", "Search Keyword"),
            ("filter", "Filter"),
            ("sort_order", "Sort Order"),
            ("sequence", "Sequence")
        ])

        # Environment Details Section
        st.subheader("🔹 Environment Details")
        env_data = create_env_section()

        # Consumer Information Section
        st.subheader("🔹 Consumer Information")
        consumer_data = create_input_section("consumer", [
            ("client_id", "Client ID"),
            ("name", "Consumer Name"),
            ("version", "Version"),
            ("platform", "Platform"),
            ("device", "Device"),
            ("os_version", "OS Version"),
            ("app_store_id", "App Store ID")
        ])

        # User Subscription Details Section
        st.subheader("🔹 User Subscription Details")
        user_data = create_input_section("user", [
            ("service_code", "Service Code"),
            ("service_level", "Service Level")
        ])

        # Transaction Details Section
        st.subheader("🔹 Transaction Details")
        trn_data = create_input_section("trn", [
            ("number", "Transaction Number"),
            ("product", "Product"),
            ("quantity", "Quantity"),
            ("amount", "Amount")
        ])

        # Experimentation Section
        st.subheader("🔹 Experimentation Details")
        exp_data = create_input_section("exp", [
            ("request_guid", "Request GUID"),
            ("response_guid", "Response GUID"),
            ("surface_id", "Surface ID"),
            ("campaign_id", "Campaign ID"),
            ("variation_id", "Variation ID"),
            ("action_block_id", "Action Block ID"),
            ("container_id", "Container ID"),
            ("treatment_id", "Treatment ID"),
            ("control_group_id", "Control Group ID"),
            ("experience_id", "Experience ID")
        ])

        # Context Section
        st.subheader("🔹 Context Information")
        context_col1, context_col2, context_col3 = st.columns(3)
        with context_col1:
            context_guid = st.text_input("Context GUID")
        with context_col2:
            context_init = st.text_input("Context Init")
        with context_col3:
            context_params = st.text_input("Context Params")

        # Entity Information Section
        st.subheader("🔹 Entity Information")
        entity_data = create_input_section("entity", [
            ("ims", "IMS"),
            ("ngl", "NGL"),
            ("device", "Device"),
            ("env", "Environment"),
            ("source", "Source"),
            ("event", "Event")
        ])

        # Custom Information Section
        st.subheader("🔹 Custom Information")
        custom_col1, custom_col2, custom_col3 = st.columns(3)
        with custom_col1:
            custom_params = st.text_input("Custom Params")
        with custom_col2:
            custom_content_params = st.text_input("Custom Content Params")
        with custom_col3:
            custom_feedback_comments = st.text_input("Custom Feedback Comments")

        # Form submission
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submitted = st.form_submit_button("📤 Submit Full Log Event", use_container_width=True)

    # Handle form submission
    if submitted:
        # Validate required fields
        if not all([description, property_key, created_by]):
            st.error("❌ Please fill in all required fields (Description, Property Key, Created By)")
            return

        # Prepare event data
        event_data_dict = {
            "description": description,
            "reference": reference,
            "dev": dev,
            "qe": qe,
            "data": data,
            "property_key": property_key,
            "created_by": created_by,
            "created_at": datetime.now().isoformat(),
            
            # Event data
            **{f"event_{k}": v for k, v in event_data.items()},
            
            # Source data
            **{f"source_{k}": v for k, v in source_data.items()},
            
            # Content data
            **{f"content_{k}": v for k, v in content_data.items()},
            
            # UI data
            **{f"ui_{k}": v for k, v in ui_data.items()},
            
            # Environment data
            **{f"env_{k}": v for k, v in env_data.items()},
            
            # Consumer data
            **{f"consumer_{k}": v for k, v in consumer_data.items()},
            
            # User data
            **{f"user_{k}": v for k, v in user_data.items()},
            
            # Transaction data
            **{f"trn_{k}": v for k, v in trn_data.items()},
            
            # Experimentation data
            **{f"exp_{k}": v for k, v in exp_data.items()},
            
            # Context data
            "context_guid": context_guid,
            "context_init": context_init,
            "context_params": context_params,
            
            # Entity data
            **{f"entity_{k}": v for k, v in entity_data.items()},
            
            # Custom data
            "custom_params": custom_params,
            "custom_content_params": custom_content_params,
            "custom_feedback_comments": custom_feedback_comments
        }

        try:
            # Insert log event
            insert_log(event_data_dict, created_by=created_by)
            st.success("✅ Full log event saved successfully!")
            
            # Show summary
            with st.expander("📋 Event Summary"):
                st.json({k: v for k, v in event_data_dict.items() if v})
                
        except Exception as e:
            st.error(f"❌ Error saving log event: {str(e)}")


def create_input_section(section_name, fields):
    """Create a section of input fields organized in columns"""
    data = {}
    
    # Organize fields in columns for better layout
    num_cols = min(3, len(fields))
    cols = st.columns(num_cols)
    
    for i, (key, label) in enumerate(fields):
        with cols[i % num_cols]:
            data[key] = st.text_input(f"{label}", key=f"{section_name}_{key}")
    
    return data


def create_env_section():
    """Create environment section with grouped inputs"""
    env_data = {}
    
    # Group environment fields
    env_groups = {
        "fw": ["name", "version"],
        "com": ["name", "version"],
        "svc": ["name", "version"],
        "api": ["name", "version"]
    }
    
    for group, keys in env_groups.items():
        st.write(f"**{group.upper()}**")
        cols = st.columns(len(keys))
        for i, key in enumerate(keys):
            with cols[i]:
                env_data[f"{group}_{key}"] = st.text_input(
                    f"{key.title()}", 
                    key=f"env_{group}_{key}"
                )
    
    return env_data


# Optional: Add data export functionality
def export_event_template():
    """Export a template for bulk event creation"""
    template = {
        "description": "",
        "reference": "",
        "dev": "",
        "qe": "",
        "data": "",
        "property_key": "",
        "created_by": "",
        # Add other fields as needed
    }
    
    st.download_button(
        label="📥 Download Event Template",
        data=json.dumps(template, indent=2),
        file_name="log_event_template.json",
        mime="application/json"
    )
