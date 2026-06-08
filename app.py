import streamlit as st
import pandas as pd
import os
import time

# ==============================================================================
# 1. ENTERPRISE PAGE ARCHITECTURE & THEME CODES
# ==============================================================================
st.set_page_config(
    page_title="Arledge Hub | Verical Operations", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS Inject for UI Depth
st.markdown("""
    <style>
        /* Global Background & Typography Softening */
        .stApp { background-color: #0f172a; color: #f8fafc; }
        
        /* Premium Card styling */
        div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] {
            background-color: #1e293b;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            border: 1px solid #334155;
            margin-bottom: 20px;
        }
        
        /* Input Field Overrides */
        .stTextInput input, .stSelectbox div[data-baseweb="select"] {
            background-color: #0f172a !important;
            border: 1px solid #475569 !important;
            color: #f8fafc !important;
            border-radius: 8px !important;
        }
        
        /* Metric Styling Tuning */
        div[data-testid="stMetricValue"] { font-size: 32px !important; font-weight: 700 !important; color: #38bdf8 !important; }
        div[data-testid="stMetricLabel"] { color: #94a3b8 !important; text-transform: uppercase; font-size: 11px !important; letter-spacing: 0.1em; }
        
        /* Hide Default Streamlit Branding */
        #MainMenu, footer, header { visibility: hidden; }
    </style>
""", unsafe_allowed_html=True)

# ==============================================================================
# 2. ROBUST SESSION STATE MANAGEMENT
# ==============================================================================
if "auth_state" not in st.session_state:
    st.session_state["auth_state"] = {"logged_in": False, "email": "", "role": "User"}

# ==============================================================================
# 3. COMPACT HIGH-END LOGIN PANEL
# ==============================================================================
def render_login():
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.write("")
        st.write("")
        st.markdown("<h1 style='text-align: center; color: #38bdf8; font-size: 42px; font-weight:800; margin-bottom:0;'>A R L E D G E</h1>", unsafe_allowed_html=True)
        st.markdown("<p style='text-align: center; color: #64748b; font-size: 14px; letter-spacing:0.2em; text-transform:uppercase; margin-bottom:40px;'>Operations Management Hub</p>", unsafe_allowed_html=True)
        
        with st.container():
            email = st.text_input("Corporate Email Address", placeholder="name@arrow.com")
            password = st.text_input("Access Password", type="password", placeholder="••••••••")
            
            st.write("")
            if st.button("Authenticate Session", use_container_width=True, type="primary"):
                # System User Matrix
                allowed_users = ["yahya.ouarach@arrow.com", "mafernandez@arrow.com"]
                if email in allowed_users and password == "Arrow2026!":
                    st.session_state["auth_state"] = {
                        "logged_in": True,
                        "email": email,
                        "role": "Admin" if email == "yahya.ouarach@arrow.com" else "User"
                    }
                    st.toast("Security handshake complete. Welcome back.", icon="🔐")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("Authentication rejected. Verify credentials and try again.")

# ==============================================================================
# 4. CORE DATA LAYER ENGINE
# ==============================================================================
@st.cache_data(ttl=600)
def fetch_master_data():
    if os.path.exists("data.csv"):
        try:
            return pd.read_csv("data.csv")
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()

# ==============================================================================
# 5. APPLICATION SHELL INTERFACE
# ==============================================================================
if not st.session_state["auth_state"]["logged_in"]:
    render_login()
else:
    # --- Sidebar Control Matrix ---
    st.sidebar.markdown("<h2 style='color:#38bdf8; margin-bottom:5px;'>ARLEDGE HUB</h2>", unsafe_allowed_html=True)
    st.sidebar.markdown(f"<p style='color:#64748b; font-size:12px;'>Active Session: {st.session_state['auth_state']['email']}</p>", unsafe_allowed_html=True)
    st.sidebar.write("")
    
    # Context-driven navigation
    navigation_options = ["📋 Knowledge Base Engine"]
    if st.session_state["auth_state"]["role"] == "Admin":
        navigation_options.append("🛠️ Systems Admin Control")
        
    current_view = st.sidebar.radio("Platform Environment", navigation_options)
    
    st.sidebar.v_spacer(height="long")
    st.sidebar.divider()
    if st.sidebar.button("Terminate Session", use_container_width=True):
        st.session_state["auth_state"] = {"logged_in": False, "email": "", "role": "User"}
        st.rerun()

    # Fetch Data State
    df = fetch_master_data()

    # ==========================================================================
    # VIEW A: KNOWLEDGE BASE ENGINE (High-End User Dashboard)
    # ==========================================================================
    if current_view == "📋 Knowledge Base Engine":
        st.markdown("<h1 style='font-size:32px; font-weight:700; margin-bottom:5px;'>Line Operations & Logistics Lookup</h1>", unsafe_allowed_html=True)
        st.markdown("<p style='color:#94a3b8; font-size:15px; margin-bottom:30px;'>Query verified operating procedures, system parameters, and strategic rationale across global supply environments.</p>", unsafe_allowed_html=True)

        if not df.empty and "Process" in df.columns:
            # High-Impact Performance Metrics Band
            total_processes = len(df["Process"].unique())
            systems_tracked = len(df["System"].dropna().unique()) if "System" in df.columns else 0
            
            m1, m2, m3 = st.columns(3)
            with m1: st.metric("Monitored Operational Processes", f"{total_processes} Active")
            with m2: st.metric("Linked Core Infrastructures", f"{systems_tracked} Platforms")
            with m3: st.metric("Data Integrity Status", "Optimal (2026)")
            
            st.write("")
            
            # Smart Search Filter Row
            col_search, col_select = st.columns([1.5, 2])
            
            with col_search:
                search_term = st.text_input("🔍 Global Keyword Filter", placeholder="Type keywords (e.g., Unity, Reno, Email)...")
            
            # Dynamically filter options based on search terms
            if search_term:
                search_mask = df.apply(lambda r: r.astype(str).str.contains(search_term, case=False).any(), axis=1)
                filtered_scope = df[search_mask]
            else:
                filtered_scope = df
                
            with col_select:
                process_list = [""] + list(filtered_scope["Process"].unique())
                selected_process = st.selectbox(
                    "🎯 Targeted Process Execution Node", 
                    options=process_list, 
                    index=0,
                    placeholder="Initialize process inquiry selection..."
                )

            # Deep Visual Row Detail Parsing
            if selected_process:
                st.divider()
                process_data = df[df["Process"] == selected_process].iloc[0]
                
                st.markdown(f"<h3 style='color:#38bdf8; font-size:22px;'>Operational Profile: {selected_process}</h3>", unsafe_allowed_html=True)
                
                # Split structural architecture layout
                layout_left, layout_right = st.columns([1, 1.2])
                
                with layout_left:
                    st.markdown("#### `System Infrastructure`")
                    st.info(f"**Associated Platform:** {process_data.get('System', 'Unassigned Structure')}")
                    
                    st.markdown("#### `Operational Rationale`")
                    st.success(f"{process_data.get('Rationale', 'No rationale documentation currently structuralized.')}")
                
                with layout_right:
                    st.markdown("#### `Execution Work Instructions`")
                    st.warning(f"{process_data.get('Instructions', 'No active work instructions mapped.')}")
                    
                    st.markdown(f"<p style='color:#64748b; font-size:12px; font-style:italic;'>Data Source Reference Asset: {process_data.get('File_Source', 'System Master Log')}</p>", unsafe_allowed_html=True)
                    
                    # Enterprise PDF Downloader Hook
                    sop_filepath = f"sops/{selected_process}.pdf"
                    if os.path.exists(sop_filepath):
                        with open(sop_filepath, "rb") as pdf_blob:
                            st.download_button(
                                label="📂 Download Official SOP Blueprint (PDF)", 
                                data=pdf_blob, 
                                file_name=f"SOP_{selected_process}.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
            else:
                st.write("")
                st.write("")
                st.markdown("""
                    <div style='text-align: center; padding: 40px; border: 2px dashed #334155; border-radius: 12px;'>
                        <p style='color: #64748b; font-size: 16px; margin-bottom: 0;'>System standing by. Use the filter controls above to securely fetch specific operational directives.</p>
                    </div>
                """, unsafe_allowed_html=True)
        else:
            st.error("System Matrix Error: The operational dataset 'data.csv' is empty or corrupt. Please contact system admin.")

    # ==========================================================================
    # VIEW B: SYSTEMS ADMIN CONTROL (The Content Injection Dashboard)
    # ==========================================================================
    elif current_view == "🛠️ Systems Admin Control":
        st.markdown("<h1 style='font-size:32px; font-weight:700; margin-bottom:5px;'>Systems Infrastructure Administration</h1>", unsafe_allowed_html=True)
        st.markdown("<p style='color:#94a3b8; font-size:15px; margin-bottom:30px;'>Hot-swap live application layers, upload fresh relational master rows, or ingest binary corporate documentation files directly.</p>", unsafe_allowed_html=True)
        
        adm_c1, adm_c2 = st.columns(2)
        
        with adm_c1:
            st.markdown("### `Database Transaction Node`")
            st.write("Upload an updated master ledger. This action overrides the production instance immediately.")
            new_data_file = st.file_uploader("Ingest 'data.csv' file", type="csv")
            if new_data_file:
                try:
                    df_verify = pd.read_csv(new_data_file)
                    df_verify.to_csv("data.csv", index=False)
                    st.success("Transaction structuralized successfully. Master database updated.")
                    st.cache_data.clear() # Clear cache memory to force instant update
                except Exception as csv_err:
                    st.error(f"Transaction aborted due to processing exception: {csv_err}")

        with adm_c2:
            st.markdown("### `SOP Digital Asset Ingestion`")
            st.write("Ingest verified process blueprints directly into production file paths mapping to process naming specs.")
            new_binary_doc = st.file_uploader("Ingest PDF Procedure Documentation", type="pdf")
            if new_binary_doc:
                if not os.path.exists("sops"):
                    os.makedirs("sops")
                target_destination = os.path.join("sops", new_binary_doc.name)
                with open(target_destination, "wb") as storage_hook:
                    storage_hook.write(new_binary_doc.getbuffer())
                st.success(f"Asset deployed cleanly to cloud directory path: {new_binary_doc.name}")
