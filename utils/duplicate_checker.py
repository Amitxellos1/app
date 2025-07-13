from utils.delta_utils import read_table
from config import TABLE_LOGS
from fuzzywuzzy import fuzz
import pandas as pd

def check_for_duplicates(new_event_name, threshold=80):
    try:
        existing_logs = read_table(TABLE_LOGS).select("event_name").toPandas()
        similar = []

        for _, row in existing_logs.iterrows():
            similarity = fuzz.token_sort_ratio(new_event_name.lower(), row['event_name'].lower())
            if similarity >= threshold:
                similar.append({
                    "existing_event": row['event_name'],
                    "similarity": similarity
                })

        return pd.DataFrame(similar).sort_values(by="similarity", ascending=False)

    except Exception as e:
        return pd.DataFrame()
