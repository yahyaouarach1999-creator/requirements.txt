import streamlit as st
import pandas as pd
import os

# ==============================================================================
# 1. PAGE ARCHITECTURE
# ==============================================================================
st.set_page_config(page_title="Arledge Hub", layout="wide")

# Simplified UI Enhancement (Avoids the previous TypeError)
st.markdown("""
    <style>
    .main { background-color: #0f172a; color: #f8fafc; }
    .stMetric { background-color: #1e293b; padding: 15px; border-radius: 10px; border: 1px solid #334155; }
    </style>
    """, unsafe_allowed_html=True)

# ==============================================================================
# 2. SESSION STATE
# ==============================================================================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_role" not in st.session_state:
    st.session_state["user_role"] = "User"

# ==============================================================================
# 3. LOGIN INTERFACE
# ==============================================================================
def login():
    st.title("A R L E D G E")
    st.subheader("Operations Management Hub")
    
    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if email in ["yahya.ouarach@arrow.com", "mafernandez@arrow.com"] and password == "Arrow2026!":
            st.session_state["logged_in"] = True
            st.session_state["user_role"] = "Admin" if "yahya" in email else "User"
            st.rerun()
        else:
            st.error("Invalid credentials.")

# ==============================================================================
# 4. MAIN APPLICATION
# ==============================================================================
if not st.session_state["logged_in"]:
    login()
else:
    # Sidebar Navigation
    st.sidebar.title("Arledge Hub")
    mode = st.sidebar.radio("Navigation", ["Knowledge Base", "Admin Dashboard"])
    
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.rerun()

    # Load Data
    @st.cache_data
    def get_data():
        if os.path.exists("data.csv"):
            return pd.read_csv("data.csv")
        return pd.DataFrame()

    df = get_data()

    if mode == "Knowledge Base":
        st.title("Line Operations & Logistics")
        
        if not df.empty:
            # Stats Bar
            m1, m2 = st.columns(2)
            m1.metric("Active Processes", len(df))
            m2.metric("System Status", "Live")

            # Search & Select
            search = st.text_input("🔍 Quick Search", placeholder="Type to filter...")
            
            # Filter logic
            if search:
                df = df[df.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]

            selected = st.selectbox("Select Process", [""] + list(df["Process"].unique()))

            if selected:
                data = df[df["Process"] == selected].iloc[0]
                st.divider()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"**System:** {data.get('System', 'N/A')}")
                    st.success(f"**Rationale:** {data.get('Rationale', 'N/A')}")
                with col2:
                    st.warning(f"**Instructions:**\n{data.get('Instructions', 'N/A')}")
                    
                    # PDF Check
                    pdf_path = f"sops/{selected}.pdf"
                    if os.path.exists(pdf_path):
                        with open(pdf_path, "rb") as f:
                            st.download_button("Download SOP PDF", f, file_name=f"{selected}.pdf")
        else:
            st.info("No data found. Admin needs to upload data.csv.")

    elif mode == "Admin Dashboard":
        if st.session_state["user_role"] == "Admin":
            st.title("Admin Control")
            
            up_csv = st.file_uploader("Upload data.csv", type="csv")
            if up_csv:
                pd.read_csv(up_csv).to_csv("data.csv", index=False)
                st.success("CSV Updated!")
                st.cache_data.clear()

            up_pdf = st.file_uploader("Upload SOP (PDF)", type="pdf")
            if up_pdf:
                if not os.path.exists("sops"): os.makedirs("sops")
                with open(f"sops/{up_pdf.name}", "wb") as f:
                    f.write(up_pdf.getbuffer())
                st.success("PDF Saved!")
        else:
            st.error("Access Denied.")
