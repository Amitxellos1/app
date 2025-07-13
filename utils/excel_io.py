import pandas as pd
from utils.db import fetch_logs, insert_log

def export_logs(template=False):
    if template:
        cols = ['name','description','category','module','severity','version','created_by']
        return pd.DataFrame(columns=cols)
    else:
        return fetch_logs("", "")

def import_logs(uploaded):
    df = pd.read_excel(uploaded, engine='openpyxl')
    report = []
    for idx, row in df.iterrows():
        need = ['name','description','category','module','severity','version','created_by']
        if not all(col in row for col in need):
            report.append(f"Row {idx+1}: missing columns")
            continue
        try:
            insert_log(*[row[c] for c in need])
            report.append(f"Row {idx+1}: OK")
        except Exception as e:
            report.append(f"Row {idx+1}: FAILED – {e}")
    success = not any("FAILED" in r for r in report)
    return success, "\n".join(report)
