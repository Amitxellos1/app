import streamlit as st
from utils.db import insert_log

def show_define_logs():
    st.title("📝 Define Full Log Event")

    with st.form("define_full_log_form"):
        st.subheader("🔹 General Information")
        when = st.date_input("When")
        description = st.text_area("Description")
        reference = st.text_input("Reference (if any)")
        dev, qe, data = st.columns(3)
        dev = dev.text_input("Dev")
        qe = qe.text_input("QE")
        data = data.text_input("Data")
        property_key = st.text_input("Property Key")

        st.subheader("🔹 Event Details")
        event = {}
        for key in [
            "guid", "coll_dts", "context_guid", "context_sequence",
            "dts_start", "dts_end", "workflow", "category", "subcategory",
            "type", "subtype", "user_guid", "offline", "ip", "user_agent",
            "language", "device_guid", "session_guid", "error_code",
            "error_type", "error_desc", "cloud_id", "count", "value",
            "pagename", "mcid_guid", "build", "url", "referrer",
            "idp", "org_guid", "connection"
        ]:
            event[key] = st.text_input(f"event.{key}")

        st.subheader("🔹 Source Information")
        source = {}
        for key in ["client_id", "name", "version", "platform", "device", "os_version", "app_store_id"]:
            source[key] = st.text_input(f"source.{key}")

        st.subheader("🔹 Content Details")
        content = {}
        for key in ["id", "name", "type", "size", "extension", "mimetype", "category", "status", "action", "author"]:
            content[key] = st.text_input(f"content.{key}")

        st.subheader("🔹 UI Details")
        ui = {}
        for key in ["view_type", "search_keyword", "filter", "sort_order", "sequence"]:
            ui[key] = st.text_input(f"ui.{key}")

        st.subheader("🔹 Environment Details")
        env = {}
        for group, keys in {
            "fw": ["name", "version"],
            "com": ["name", "version"],
            "svc": ["name", "version"],
            "api": ["name", "version"]
        }.items():
            for key in keys:
                env[f"{group}_{key}"] = st.text_input(f"env.{group}.{key}")

        st.subheader("🔹 Consumer Information")
        consumer = {}
        for key in ["client_id", "name", "version", "platform", "device", "os_version", "app_store_id"]:
            consumer[key] = st.text_input(f"consumer.{key}")

        st.subheader("🔹 User Subscription Details")
        user = {}
        for key in ["service_code", "service_level"]:
            user[key] = st.text_input(f"user.{key}")

        st.subheader("🔹 Transaction Details")
        trn = {}
        for key in ["number", "product", "quantity", "amount"]:
            trn[key] = st.text_input(f"trn.{key}")

        st.subheader("🔹 Experimentation (exp.*) Info")
        exp = {}
        for key in [
            "request_guid", "response_guid", "surface_id", "campaign_id", "variation_id",
            "action_block_id", "container_id", "treatment_id", "control_group_id", "experience_id"
        ]:
            exp[key] = st.text_input(f"exp.{key}")

        st.subheader("🔹 Context")
        context_guid = st.text_input("context.guid")
        context_init = st.text_input("context.init")
        context_params = st.text_input("context.params")

        st.subheader("🔹 Entity Information")
        entity = {}
        for key in ["ims", "ngl", "device", "env", "source", "event"]:
            entity[key] = st.text_input(f"entity.{key}")

        st.subheader("🔹 Custom Information")
        custom_params = st.text_input("custom.params")
        custom_content_params = st.text_input("custom.content_params")
        custom_feedback_comments = st.text_input("custom.feedback_comments")

        st.subheader("🔹 Created By")
        created_by = st.text_input("Created By", value="PM/DS Name")

        submitted = st.form_submit_button("Submit Full Log Event")

    if submitted:
        event_data = {
            "when": str(when),
            "description": description,
            "reference": reference,
            "dev": dev,
            "qe": qe,
            "data": data,
            "property_key": property_key,
            "created_by": created_by,
            # Event
            **{f"event_{k}": v for k, v in event.items()},
            # Source
            **{f"source_{k}": v for k, v in source.items()},
            # Content
            **{f"content_{k}": v for k, v in content.items()},
            # UI
            **{f"ui_{k}": v for k, v in ui.items()},
            # Env
            **{f"env_{k}": v for k, v in env.items()},
            # Consumer
            **{f"consumer_{k}": v for k, v in consumer.items()},
            # User
            **{f"user_{k}": v for k, v in user.items()},
            # Transaction
            **{f"trn_{k}": v for k, v in trn.items()},
            # Exp
            **{f"exp_{k}": v for k, v in exp.items()},
            # Context
            "context_guid": context_guid,
            "context_init": context_init,
            "context_params": context_params,
            # Entity
            **{f"entity_{k}": v for k, v in entity.items()},
            # Custom
            "custom_params": custom_params,
            "custom_content_params": custom_content_params,
            "custom_feedback_comments": custom_feedback_comments
        }

        insert_log(event_data, created_by=created_by)
        st.success("✅ Full log event saved successfully!")
