import io
import streamlit as st
from utils.excel_io import export_logs, import_logs

def to_excel_bytes(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return output.getvalue()

def show():
    st.title("📤📥 Import / Export Logs")

    st.markdown("### 📥 Export Logs")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬇️ Download Template"):
            df_template = export_logs(template=True)
            st.download_button(
                label="Download Blank Template",
                data=to_excel_bytes(df_template),
                file_name="logs_template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    with col2:
        if st.button("⬇️ Export All Logs"):
            df_all = export_logs()
            st.download_button(
                label="Download All Logs",
                data=to_excel_bytes(df_all),
                file_name="logs_data_export.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    st.markdown("### 📤 Import Logs")

    uploaded_file = st.file_uploader("Upload logs Excel file (.xlsx)", type="xlsx")

    if uploaded_file:
        created_by = st.text_input("Your Name (for audit trail)", value="user")
        if st.button("📤 Import Logs"):
            success, report = import_logs(uploaded_file, created_by=created_by)

            if success:
                st.success("✅ All rows imported successfully!")
            else:
                st.error("⚠️ Some rows failed to import. See below.")

            st.text_area("📋 Import Report", report, height=250)
