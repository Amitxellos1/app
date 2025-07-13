import streamlit as st
from pages import define_logs, search_logs, version_control, import_export

st.set_page_config(page_title="Logs Manager", layout="wide")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Define Logs", "Search Logs", "Version Control", "Import/Export"])

if page == "Define Logs":
    define_logs.show()
elif page == "Search Logs":
    search_logs.show()
elif page == "Version Control":
    version_control.show()
elif page == "Import/Export":
    import_export.show()
