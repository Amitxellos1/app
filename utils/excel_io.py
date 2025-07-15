import pandas as pd
from utils.db import fetch_logs, insert_log, columns

def export_logs(template=False):
    if template:
        # Export only the main input fields as blank template (excluding created_by, created_at, etc.)
        exclude_cols = ["created_by", "created_at", "updated_at"]
        export_cols = [col for col in columns if col not in exclude_cols]
        return pd.DataFrame(columns=export_cols)
    else:
        # Export existing logs from database
        return fetch_logs()

def import_logs(uploaded_file, created_by="user"):
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    report = []
    total_rows = len(df)

    # Expecting columns from the template
    expected_cols = [col for col in columns if col not in ["created_by", "created_at", "updated_at"]]

    # Validate columns present
    missing_cols = [col for col in expected_cols if col not in df.columns]
    if missing_cols:
        return False, f"❌ Missing columns in uploaded file: {', '.join(missing_cols)}"

    # Iterate rows
    for idx, row in df.iterrows():
        event_data = {col: str(row[col]) if pd.notnull(row[col]) else "" for col in expected_cols}
        try:
            insert_log(event_data, created_by=created_by)
            report.append(f"Row {idx + 1}/{total_rows}: ✅ Imported")
        except Exception as e:
            report.append(f"Row {idx + 1}/{total_rows}: ❌ FAILED – {str(e)}")

    success = all("✅" in line for line in report)
    return success, "\n".join(report)
