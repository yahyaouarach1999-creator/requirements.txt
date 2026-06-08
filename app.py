import streamlit as st
import pandas as pd
import os

# ==============================================================================
# 1. PAGE ARCHITECTURE
# ==============================================================================
st.set_page_config(page_title="Arledge Hub", layout="wide")

# ==============================================================================
# 2. ROBUST SESSION STATE INITIALIZATION
# ==============================================================================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_role" not in st.session_state:
    st.session_state["user_role"] = "User"
if "user_email" not in st.session_state:
    st.session_state["user_email"] = ""

# ==============================================================================
# 3. SECURE AUTHENTICATION INTERFACE
# ==============================================================================
def render_login_screen():
    st.title("🛡️ ARLEDGE HUB")
    st.caption("Verical Operations & Logistics Management Platform")
    st.divider()
    
    with st.form("login_form"):
        email_input = st.text_input("Corporate Email Address", placeholder="username@arrow.com")
        password_input = st.text_input("Access Password", type="password", placeholder="••••••••")
        submit_button = st.form_submit_button("Authenticate Session", use_container_width=True)
        
        if submit_button:
            authorized_emails = ["yahya.ouarach@arrow.com", "mafernandez@arrow.com"]
            if email_input.lower() in authorized_emails and password_input == "Arrow2026!":
                st.session_state["logged_in"] = True
                st.session_state["user_email"] = email_input
                st.session_state["user_role"] = "Admin" if "yahya" in email_input.lower() else "User"
                st.rerun()
            else:
                st.error("Authentication rejected. Please check credentials.")

# ==============================================================================
# 4. MAIN ENGINE APPLICATION LOGIC
# ==============================================================================
if not st.session_state["logged_in"]:
    render_login_screen()
else:
    # --- NAVIGATION ARCHITECTURE ---
    st.sidebar.title("💎 Arledge Hub")
    st.sidebar.caption(f"Connected: {st.session_state['user_email']}")
    
    nav_options = ["📋 Knowledge Base Engine"]
    if st.session_state["user_role"] == "Admin":
        nav_options.append("🛠️ Systems Admin Control")
        
    current_view = st.sidebar.radio("Platform Environment", nav_options)
    
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.divider()
    
    if st.sidebar.button("Terminate Session", use_container_width=True):
        st.session_state["logged_in"] = False
        st.session_state["user_role"] = "User"
        st.session_state["user_email"] = ""
        st.rerun()

    # --- DATA EXTRACTION LAYER ---
    @st.cache_data
    def load_operational_data():
        if os.path.exists("data.csv"):
            try:
                return pd.read_csv("data.csv")
            except Exception as e:
                st.sidebar.error(f"Data Read Failure: {e}")
                return pd.DataFrame()
        return pd.DataFrame()

    df_master = load_operational_data()

    # ==========================================================================
    # SYSTEM VIEW A: KNOWLEDGE BASE ENGINE (SEARCH-DRIVEN INTERFACE)
    # ==========================================================================
    if current_view == "📋 Knowledge Base Engine":
        st.title("Line Operations & Logistics Lookup")
        st.write("Query verified operating procedures, system parameters, and strategic rationales.")
        st.divider()
        
        if not df_master.empty:
            # --- HEART-CENTRIC METRICS OVERHAUL ---
            m1, m2 = st.columns(2)
            with m1:
                st.metric(label="🎯 LOGISTICS PROCEDURES GUARDED", value=f"{len(df_master['Process'].unique()) if 'Process' in df_master.columns else 0} SOPs Ready")
            with m2:
                st.metric(label="✨ TEAM OPERATIONAL READINESS", value="Fully Prepared")
                
            st.write("")
            
            # --- FIXED DUAL-LAYER FILTER ENGINE ---
            search_col, select_col = st.columns([1.5, 2])
            
            with search_col:
                search_term = st.text_input("🔍 Filter by Keyword", placeholder="Type keywords (e.g., Unity, Reno)...")
            
            # Filter rows based on search term
            if search_term:
                search_mask = df_master.apply(lambda r: r.astype(str).str.contains(search_term, case=False).any(), axis=1)
                df_filtered = df_master[search_mask]
            else:
                df_filtered = df_master
                
            with select_col:
                if "Process" in df_filtered.columns and not df_filtered.empty:
                    process_options = [""] + sorted(list(df_filtered["Process"].dropna().unique()))
                else:
                    process_options = [""]
                
                # Check if we should auto-select the first valid item if filtering narrow scopes
                selected_process = st.selectbox(
                    "🎯 Targeted Process Node Lookup",
                    options=process_options,
                    index=0,
                    placeholder="Choose an item to run parsing inquiry..."
                )

            # Detail Render Block
            if selected_process and selected_process != "":
                st.divider()
                # Pull exact record from master to ensure matching is completely authentic
                process_data = df_master[df_master["Process"] == selected_process].iloc[0]
                
                st.subheader(f"Operational Specifications: {selected_process}")
                
                left_panel, right_panel = st.columns([1, 1.2])
                
                with left_panel:
                    st.info(f"**Associated Infrastructure Platform:**\n\n{process_data.get('System', 'N/A')}")
                    st.success(f"**Strategic Process Rationale:**\n\n{process_data.get('Rationale', 'N/A')}")
                
                with right_panel:
                    st.warning(f"**Execution Work Instructions:**\n\n{process_data.get('Instructions', 'N/A')}")
                    st.caption(f"Source Reference Ledger Asset: {process_data.get('File_Source', 'System Log File')}")
                    
                    # Direct Link Hook for local SOP PDF assets
                    pdf_target_path = f"sops/{selected_process}.pdf"
                    if os.path.exists(pdf_target_path):
                        with open(pdf_target_path, "rb") as pdf_stream:
                            st.download_button(
                                label="📂 Download Official SOP Blueprint Document (PDF)",
                                data=pdf_stream,
                                file_name=f"SOP_{selected_process}.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
            else:
                st.write("")
                st.info("System Ready. Enter a query or select a target operational node above to load data details safely.")
        else:
            st.error("System Matrix Mismatch: The local ledger asset 'data.csv' is empty or missing. Please initialize dataset via Admin Dashboard.")

    # ==========================================================================
    # SYSTEM VIEW B: SYSTEMS ADMIN CONTROL (UPLOADER DASHBOARD)
    # ==========================================================================
    elif current_view == "🛠️ Systems Admin Control":
        st.title("Systems Infrastructure Administration")
        st.write("Deploy framework changes, append fresh transaction rows, or clear server caches.")
        st.divider()
        
        left_upload_col, right_upload_col = st.columns(2)
        
        with left_upload_col:
            st.subheader("Update Master Database")
            st.write("Upload a modern structured layout of your files. This overrides current entries instantly.")
            uploaded_csv_file = st.file_uploader("Upload New production data.csv", type="csv")
            if uploaded_csv_file:
                try:
                    df_check = pd.read_csv(uploaded_csv_file)
                    df_check.to_csv("data.csv", index=False)
                    st.success("Master infrastructure update transaction complete.")
                    st.cache_data.clear() 
                except Exception as ex_err:
                    st.error(f"Transaction failure: {ex_err}")
                    
        with right_upload_col:
            st.subheader("SOP Digital Asset Ingestion")
            st.write("Ingest dynamic document layouts linking explicitly to database items.")
            uploaded_pdf_file = st.file_uploader("Upload SOP Blueprint PDF", type="pdf")
            if uploaded_pdf_file:
                if not os.path.exists("sops"):
                    os.makedirs("sops")
                with open(os.path.join("sops", uploaded_pdf_file.name), "wb") as output_disk_file:
                    output_disk_file.write(uploaded_pdf_file.getbuffer())
                st.success(f"Asset deployed: {uploaded_pdf_file.name}")
