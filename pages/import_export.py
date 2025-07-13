import streamlit as st
from utils.excel_io import export_logs, import_logs

def show():
    st.title("Import / Export Logs")

    if st.button("Download Template"):
        df = export_logs(template=True)
        st.download_button("Download", df.to_excel(index=False), "template.xlsx")

    if st.button("Export All Logs"):
        df = export_logs()
        st.download_button("Download", df.to_excel(index=False), "all_logs.xlsx")

    uploaded = st.file_uploader("Upload logs Excel", type="xlsx")
    if uploaded:
        success, report = import_logs(uploaded)
        if success:
            st.success("Import successful!")
        else:
            st.error("Import issues: " + report)
        st.write(report)
