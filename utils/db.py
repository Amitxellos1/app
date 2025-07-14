import sqlite3
import pandas as pd
from datetime import datetime

DB_FILE = "logs.db"
conn = sqlite3.connect(DB_FILE, check_same_thread=False)

columns = [
    'when', 'description', 'reference', 'dev', 'qe', 'data', 'property_key',
    'event_guid', 'event_coll_dts', 'event_context_guid', 'event_context_sequence', 'event_dts_start',
    'event_dts_end', 'event_workflow', 'event_category', 'event_subcategory', 'event_type',
    'event_subtype', 'event_user_guid', 'event_offline', 'event_ip', 'event_user_agent',
    'event_language', 'event_device_guid', 'event_session_guid', 'event_error_code', 'event_error_type',
    'event_error_desc', 'event_cloud_id', 'event_count', 'event_value', 'event_pagename',
    'event_mcid_guid', 'event_build', 'event_url', 'event_referrer', 'event_idp', 'event_org_guid',
    'source_client_id', 'source_name', 'source_version', 'source_platform', 'source_device',
    'source_os_version', 'source_app_store_id',
    'content_id', 'content_name', 'content_type', 'content_size', 'content_extension', 'content_mimetype',
    'content_category', 'content_status', 'content_action', 'content_author',
    'ui_view_type', 'ui_search_keyword', 'ui_filter', 'ui_sort_order', 'ui_sequence',
    'env_fw_name', 'env_fw_version', 'env_com_name', 'env_com_version',
    'env_svc_name', 'env_svc_version', 'env_api_name', 'env_api_version',
    'consumer_client_id', 'consumer_name', 'consumer_version', 'consumer_platform', 'consumer_device',
    'consumer_os_version', 'consumer_app_store_id',
    'user_service_code', 'user_service_level',
    'trn_number', 'trn_product', 'trn_quantity', 'trn_amount',
    'exp_request_guid', 'exp_response_guid', 'exp_surface_id', 'exp_campaign_id', 'exp_variation_id',
    'exp_action_block_id', 'exp_container_id', 'exp_treatment_id', 'exp_control_group_id', 'exp_experience_id',
    'context_guid', 'context_init', 'context_params',
    'event_connection', 'entity_ims', 'entity_ngl', 'entity_device', 'entity_env', 'entity_source', 'entity_event',
    'custom_params', 'custom_content_params', 'custom_feedback_comments',
    'created_by', 'created_at', 'updated_at'
]

def create_table():
    fields = ',\n'.join([f"{col} TEXT" for col in columns])
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS logs_definitions (
            event_row_id TEXT PRIMARY KEY,
            {fields}
        )
    """)
    conn.commit()

create_table()

def insert_log(event_data: dict, created_by="user"):
    now = datetime.utcnow().isoformat()
    event_row_id = f"event_{now.replace(':','').replace('-','').replace('.','')}"
    
    all_data = {col: event_data.get(col, "") for col in columns}
    all_data.update({
        "created_by": created_by,
        "created_at": now,
        "updated_at": now
    })

    columns_str = ", ".join(["event_row_id"] + list(all_data.keys()))
    placeholders = ", ".join(["?"] * (len(all_data) + 1))
    values = [event_row_id] + list(all_data.values())

    conn.execute(f"""
        INSERT INTO logs_definitions ({columns_str}) VALUES ({placeholders})
    """, values)
    conn.commit()

def fetch_logs(q=None, category=None):
    query = "SELECT * FROM logs_definitions WHERE 1=1"
    params = []

    if q:
        query += " AND (description LIKE ? OR event_workflow LIKE ?)"
        params += [f"%{q}%", f"%{q}%"]
    if category:
        query += " AND event_category = ?"
        params.append(category)

    return pd.read_sql_query(query, conn, params=params)

def fetch_versions(event_workflow):
    query = """
        SELECT created_by, created_at, updated_at 
        FROM logs_definitions
        WHERE event_workflow = ?
        ORDER BY created_at DESC
    """
    return pd.read_sql_query(query, conn, params=(event_workflow,))

def delete_all_logs():
    conn.execute("DELETE FROM logs_definitions")
    conn.commit()
