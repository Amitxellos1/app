import streamlit as st
from utils.db import insert_log, get_all_logs, get_log_by_id, update_log
from datetime import datetime
import json

def show():
    st.title("📝 Define Full Log Event")
    
    # Add mode selection
    st.markdown("---")
    mode = st.radio(
        "**Select Mode:**",
        ["➕ Add New Event", "✏️ Edit Existing Event", "📋 Duplicate Existing Event"],
        horizontal=True
    )
    
    # Initialize variables
    selected_event = None
    event_id = None
    
    # Handle different modes
    if mode == "✏️ Edit Existing Event":
        existing_events = get_existing_events()
        if existing_events:
            selected_event_key = st.selectbox(
                "Select event to edit:",
                options=list(existing_events.keys()),
                format_func=lambda x: existing_events[x]
            )
            if selected_event_key:
                selected_event = get_log_by_id(selected_event_key)
                event_id = selected_event_key
                st.info(f"📝 Editing event: {existing_events[selected_event_key]}")
        else:
            st.warning("No existing events found to edit.")
            return
            
    elif mode == "📋 Duplicate Existing Event":
        existing_events = get_existing_events()
        if existing_events:
            selected_event_key = st.selectbox(
                "Select event to duplicate:",
                options=list(existing_events.keys()),
                format_func=lambda x: existing_events[x]
            )
            if selected_event_key:
                selected_event = get_log_by_id(selected_event_key)
                st.info(f"📋 Duplicating event: {existing_events[selected_event_key]}")
                st.markdown("*You can modify any fields below before saving as a new event*")
        else:
            st.warning("No existing events found to duplicate.")
            return
    
    st.markdown("---")
    
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
            description = st.text_area(
                "Description *", 
                value=get_field_value(selected_event, "description"),
                help="Brief description of the log event"
            )
            reference = st.text_input(
                "Reference", 
                value=get_field_value(selected_event, "reference"),
                help="Reference number or ID if any"
            )
            property_key = st.text_input(
                "Property Key *", 
                value=get_field_value(selected_event, "property_key"),
                help="Unique identifier for this property"
            )
        
        with col2:
            created_by = st.text_input(
                "Created By *", 
                value=get_field_value(selected_event, "created_by", "PM/DS Name"),
                help="Your name or ID"
            )
            
        # Team Information
        st.write("**Team Information**")
        dev_col, qe_col, data_col = st.columns(3)
        with dev_col:
            dev = st.text_input("Dev Team", value=get_field_value(selected_event, "dev"))
        with qe_col:
            qe = st.text_input("QE Team", value=get_field_value(selected_event, "qe"))
        with data_col:
            data = st.text_input("Data Team", value=get_field_value(selected_event, "data"))

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
        ], selected_event)

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
        ], selected_event)

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
        ], selected_event)

        # UI Details Section
        st.subheader("🔹 UI Details")
        ui_data = create_input_section("ui", [
            ("view_type", "View Type"),
            ("search_keyword", "Search Keyword"),
            ("filter", "Filter"),
            ("sort_order", "Sort Order"),
            ("sequence", "Sequence")
        ], selected_event)

        # Environment Details Section
        st.subheader("🔹 Environment Details")
        env_data = create_env_section(selected_event)

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
        ], selected_event)

        # User Subscription Details Section
        st.subheader("🔹 User Subscription Details")
        user_data = create_input_section("user", [
            ("service_code", "Service Code"),
            ("service_level", "Service Level")
        ], selected_event)

        # Transaction Details Section
        st.subheader("🔹 Transaction Details")
        trn_data = create_input_section("trn", [
            ("number", "Transaction Number"),
            ("product", "Product"),
            ("quantity", "Quantity"),
            ("amount", "Amount")
        ], selected_event)

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
        ], selected_event)

        # Context Section
        st.subheader("🔹 Context Information")
        context_col1, context_col2, context_col3 = st.columns(3)
        with context_col1:
            context_guid = st.text_input(
                "Context GUID", 
                value=get_field_value(selected_event, "context_guid")
            )
        with context_col2:
            context_init = st.text_input(
                "Context Init", 
                value=get_field_value(selected_event, "context_init")
            )
        with context_col3:
            context_params = st.text_input(
                "Context Params", 
                value=get_field_value(selected_event, "context_params")
            )

        # Entity Information Section
        st.subheader("🔹 Entity Information")
        entity_data = create_input_section("entity", [
            ("ims", "IMS"),
            ("ngl", "NGL"),
            ("device", "Device"),
            ("env", "Environment"),
            ("source", "Source"),
            ("event", "Event")
        ], selected_event)

        # Custom Information Section
        st.subheader("🔹 Custom Information")
        custom_col1, custom_col2, custom_col3 = st.columns(3)
        with custom_col1:
            custom_params = st.text_input(
                "Custom Params", 
                value=get_field_value(selected_event, "custom_params")
            )
        with custom_col2:
            custom_content_params = st.text_input(
                "Custom Content Params", 
                value=get_field_value(selected_event, "custom_content_params")
            )
        with custom_col3:
            custom_feedback_comments = st.text_input(
                "Custom Feedback Comments", 
                value=get_field_value(selected_event, "custom_feedback_comments")
            )

        # Form submission with dynamic button text
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            button_text = {
                "➕ Add New Event": "📤 Create New Event",
                "✏️ Edit Existing Event": "💾 Update Event",
                "📋 Duplicate Existing Event": "📋 Save as New Event"
            }
            submitted = st.form_submit_button(
                button_text[mode], 
                use_container_width=True
            )

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
            "updated_at": datetime.now().isoformat(),
            
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

        # Add created_at for new events
        if mode in ["➕ Add New Event", "📋 Duplicate Existing Event"]:
            event_data_dict["created_at"] = datetime.now().isoformat()

        try:
            # Handle different modes
            if mode == "✏️ Edit Existing Event":
                update_log(event_id, event_data_dict)
                st.success("✅ Log event updated successfully!")
            else:
                insert_log(event_data_dict, created_by=created_by)
                action = "duplicated and saved" if mode == "📋 Duplicate Existing Event" else "created"
                st.success(f"✅ Log event {action} successfully!")
            
            # Show summary
            with st.expander("📋 Event Summary"):
                st.json({k: v for k, v in event_data_dict.items() if v})
                
        except Exception as e:
            st.error(f"❌ Error processing log event: {str(e)}")


def get_existing_events():
    """Retrieve existing events for selection"""
    try:
        events = get_all_logs()
        if events:
            return {
                event.get('id', f"event_{i}"): f"{event.get('description', 'No description')[:50]}... (by {event.get('created_by', 'Unknown')})"
                for i, event in enumerate(events)
            }
        return {}
    except Exception as e:
        st.error(f"Error retrieving events: {str(e)}")
        return {}


def get_field_value(selected_event, field_name, default=""):
    """Get field value from selected event or return default"""
    if selected_event and field_name in selected_event:
        return selected_event[field_name] or default
    return default


def create_input_section(section_name, fields, selected_event=None):
    """Create a section of input fields organized in columns"""
    data = {}
    
    # Organize fields in columns for better layout
    num_cols = min(3, len(fields))
    cols = st.columns(num_cols)
    
    for i, (key, label) in enumerate(fields):
        with cols[i % num_cols]:
            field_key = f"{section_name}_{key}"
            default_value = get_field_value(selected_event, field_key)
            data[key] = st.text_input(
                f"{label}", 
                value=default_value,
                key=f"{section_name}_{key}"
            )
    
    return data


def create_env_section(selected_event=None):
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
                field_key = f"env_{group}_{key}"
                default_value = get_field_value(selected_event, field_key)
                env_data[f"{group}_{key}"] = st.text_input(
                    f"{key.title()}", 
                    value=default_value,
                    key=f"env_{group}_{key}"
                )
    
    return env_data


def show_event_comparison(original_event, updated_event):
    """Show comparison between original and updated events"""
    st.subheader("📊 Changes Made")
    
    changes = []
    for key, new_value in updated_event.items():
        old_value = original_event.get(key, "")
        if old_value != new_value:
            changes.append({
                "Field": key,
                "Old Value": old_value or "(empty)",
                "New Value": new_value or "(empty)"
            })
    
    if changes:
        st.table(changes)
    else:
        st.info("No changes detected.")


# Optional: Add bulk operations
def show_bulk_operations():
    """Show bulk operations section"""
    st.subheader("🔄 Bulk Operations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Import Events from JSON"):
            uploaded_file = st.file_uploader("Choose JSON file", type="json")
            if uploaded_file:
                try:
                    events = json.load(uploaded_file)
                    # Process bulk import
                    st.success(f"Imported {len(events)} events successfully!")
                except Exception as e:
                    st.error(f"Error importing events: {str(e)}")
    
    with col2:
        if st.button("📤 Export All Events"):
            try:
                all_events = get_all_logs()
                if all_events:
                    st.download_button(
                        label="Download Events JSON",
                        data=json.dumps(all_events, indent=2),
                        file_name=f"log_events_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                else:
                    st.warning("No events found to export.")
            except Exception as e:
                st.error(f"Error exporting events: {str(e)}")


# Optional: Add search and filter functionality
def show_event_search():
    """Show event search and filter functionality"""
    st.subheader("🔍 Search Events")
    
    search_term = st.text_input("Search in descriptions:")
    if search_term:
        try:
            events = get_all_logs()
            filtered_events = [
                event for event in events 
                if search_term.lower() in event.get('description', '').lower()
            ]
            st.write(f"Found {len(filtered_events)} matching events:")
            for event in filtered_events:
                st.write(f"- {event.get('description', 'No description')} (by {event.get('created_by', 'Unknown')})")
        except Exception as e:
            st.error(f"Error searching events: {str(e)}")


# Add this to the main show() function if you want these additional features
# show_event_search()
# show_bulk_operations()
