import streamlit as st
from pages import define_logs, search_logs, version_control, import_export

st.set_page_config(
    page_title="Logs Manager",
    page_icon="📜",
    layout="wide"
)

# Custom CSS for better visuals
st.markdown("""
    <style>
        .main { background-color: #f8f9fa; }
        .st-expander { background: #fffbe7 !important; }
        .stAlert { background: #e3f2fd !important; }
        .big-title { font-size: 2.8rem; font-weight: 700; color: #3d3d3d; }
        .subtitle { font-size: 1.2rem; color: #555; }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "🏠 Home",
        "📝 Define Logs",
        "🔍 Search Logs",
        "📊 Version Control",
        "📤📥 Import/Export"
    ]
)

st.markdown('<div class="big-title">📜 Logs Manager</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">A collaborative tool for managing, searching, and versioning event logs.</div>', unsafe_allow_html=True)
st.write("")

if page == "🏠 Home":
    with st.expander("❓ How to use this app", expanded=True):
        st.markdown("""
        **Logs Manager** helps Product Managers, Data Scientists, and Developers coordinate event logging with ease.

        **Main Features:**
        - 📝 **Define Logs:** Create and document new event logs.
        - 🔍 **Search Logs:** Quickly find and filter logs.
        - 📊 **Version Control:** Track changes and maintain log history.
        - 📤📥 **Import/Export:** Upload or download logs as Excel files.

        👉 Use the sidebar to navigate between sections.
        """)
    st.info("👈 Select a section from the sidebar to get started: **Define Logs**, **Search Logs**, **Version Control**, or **Import/Export**.")

elif page == "📝 Define Logs":
    define_logs.show()

elif page == "🔍 Search Logs":
    search_logs.show()

elif page == "📊 Version Control":
    version_control.show()

elif page == "📤📥 Import/Export":
    import_export.show()
