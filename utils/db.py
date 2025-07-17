import sqlite3
import pandas as pd
from datetime import datetime
import os


# Create a persistent directory for your app data
DB_DIR = os.path.expanduser("~/streamlit_app_data")  # User's home directory
os.makedirs(DB_DIR, exist_ok=True)

DB_FILE = os.path.join(DB_DIR, "logs_definitions.db")
conn = sqlite3.connect(DB_FILE, check_same_thread=False)


columns = [
    'description', 'reference', 'dev', 'qe', 'data', 'property_key',
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
    create_query = f"""
        CREATE TABLE IF NOT EXISTS logs_definitions (
            event_row_id TEXT PRIMARY KEY,
            {fields}
        )
    """
    conn.execute(create_query)
    conn.commit()

create_table() 

def insert_log(event_data: dict, created_by="user"):
    now = datetime.utcnow().isoformat()
    event_row_id = f"event_{now.replace(':', '').replace('-', '').replace('.', '')}"

    # Prepare data dict with default empty strings
    all_data = {col: event_data.get(col, "") for col in columns}
    all_data["created_by"] = created_by
    all_data["created_at"] = now
    all_data["updated_at"] = now

    # SQL query preparation
    column_names = ["event_row_id"] + list(all_data.keys())
    placeholders = ", ".join(["?"] * len(column_names))
    values = [event_row_id] + list(all_data.values())

    query = f"""
        INSERT INTO logs_definitions ({", ".join(column_names)}) 
        VALUES ({placeholders})
    """

    conn.execute(query, values)
    conn.commit()

def get_all_logs():
    """
    Retrieve all log events from the database
    Returns: List of dictionaries containing all log events
    """
    try:
        query = "SELECT * FROM logs_definitions ORDER BY created_at DESC"
        cursor = conn.execute(query)
        rows = cursor.fetchall()
        
        # Get column names
        column_names = [description[0] for description in cursor.description]
        
        # Convert to list of dictionaries
        logs = []
        for row in rows:
            log_dict = dict(zip(column_names, row))
            # Use event_row_id as the main ID for consistency
            log_dict['id'] = log_dict['event_row_id']
            logs.append(log_dict)
        
        return logs
    except Exception as e:
        print(f"Error retrieving all logs: {e}")
        return []

def get_log_by_id(log_id):
    """
    Retrieve a specific log event by its ID
    Args:
        log_id (str): The event_row_id of the log event
    Returns: Dictionary containing the log event data or None if not found
    """
    try:
        query = "SELECT * FROM logs_definitions WHERE event_row_id = ?"
        cursor = conn.execute(query, (log_id,))
        row = cursor.fetchone()
        
        if row:
            # Get column names
            column_names = [description[0] for description in cursor.description]
            
            # Convert to dictionary
            log_dict = dict(zip(column_names, row))
            # Use event_row_id as the main ID for consistency
            log_dict['id'] = log_dict['event_row_id']
            return log_dict
        
        return None
    except Exception as e:
        print(f"Error retrieving log by ID {log_id}: {e}")
        return None

def update_log(log_id, event_data):
    """
    Update an existing log event
    Args:
        log_id (str): The event_row_id of the log event to update
        event_data (dict): Dictionary containing the updated event data
    """
    try:
        # Get current timestamp
        now = datetime.utcnow().isoformat()
        
        # Prepare data dict with default empty strings for missing fields
        all_data = {col: event_data.get(col, "") for col in columns}
        all_data["updated_at"] = now
        
        # Keep original created_by and created_at if not provided
        existing_log = get_log_by_id(log_id)
        if existing_log:
            all_data["created_by"] = event_data.get("created_by", existing_log.get("created_by", ""))
            all_data["created_at"] = existing_log.get("created_at", now)
        
        # Build UPDATE query
        set_clauses = []
        values = []
        
        for col in columns:
            set_clauses.append(f"{col} = ?")
            values.append(all_data[col])
        
        # Add the WHERE clause parameter
        values.append(log_id)
        
        query = f"""
            UPDATE logs_definitions 
            SET {', '.join(set_clauses)}
            WHERE event_row_id = ?
        """
        
        cursor = conn.execute(query, values)
        conn.commit()
        
        # Check if update was successful
        if cursor.rowcount > 0:
            print(f"Successfully updated log event {log_id}")
            return True
        else:
            print(f"No log event found with ID {log_id}")
            return False
            
    except Exception as e:
        print(f"Error updating log {log_id}: {e}")
        return False

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

# Additional utility functions for better database management

def get_logs_count():
    """
    Get the total count of log events
    Returns: Integer count of total log events
    """
    try:
        cursor = conn.execute("SELECT COUNT(*) FROM logs_definitions")
        count = cursor.fetchone()[0]
        return count
    except Exception as e:
        print(f"Error getting logs count: {e}")
        return 0

def get_logs_by_creator(created_by):
    """
    Get all log events created by a specific user
    Args:
        created_by (str): The creator's name/ID
    Returns: List of dictionaries containing log events
    """
    try:
        query = "SELECT * FROM logs_definitions WHERE created_by = ? ORDER BY created_at DESC"
        cursor = conn.execute(query, (created_by,))
        rows = cursor.fetchall()
        
        # Get column names
        column_names = [description[0] for description in cursor.description]
        
        # Convert to list of dictionaries
        logs = []
        for row in rows:
            log_dict = dict(zip(column_names, row))
            log_dict['id'] = log_dict['event_row_id']
            logs.append(log_dict)
        
        return logs
    except Exception as e:
        print(f"Error retrieving logs by creator {created_by}: {e}")
        return []

def search_logs(search_term):
    """
    Search for log events based on description or workflow
    Args:
        search_term (str): The term to search for
    Returns: List of dictionaries containing matching log events
    """
    try:
        query = """
            SELECT * FROM logs_definitions 
            WHERE description LIKE ? OR event_workflow LIKE ? OR property_key LIKE ?
            ORDER BY created_at DESC
        """
        search_pattern = f"%{search_term}%"
        cursor = conn.execute(query, (search_pattern, search_pattern, search_pattern))
        rows = cursor.fetchall()
        
        # Get column names
        column_names = [description[0] for description in cursor.description]
        
        # Convert to list of dictionaries
        logs = []
        for row in rows:
            log_dict = dict(zip(column_names, row))
            log_dict['id'] = log_dict['event_row_id']
            logs.append(log_dict)
        
        return logs
    except Exception as e:
        print(f"Error searching logs: {e}")
        return []

def delete_log_by_id(log_id):
    """
    Delete a specific log event by its ID
    Args:
        log_id (str): The event_row_id of the log event to delete
    Returns: Boolean indicating success
    """
    try:
        cursor = conn.execute("DELETE FROM logs_definitions WHERE event_row_id = ?", (log_id,))
        conn.commit()
        
        if cursor.rowcount > 0:
            print(f"Successfully deleted log event {log_id}")
            return True
        else:
            print(f"No log event found with ID {log_id}")
            return False
            
    except Exception as e:
        print(f"Error deleting log {log_id}: {e}")
        return False
