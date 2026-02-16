import streamlit as st
import pandas as pd
import os

# 1. PAGE SETUP
st.set_page_config(page_title="Arledge", layout="wide", page_icon="🏹")

# --- FIXED ACCESS CONTROL ---
# No more overwriting; all admins and users are in clear, separate lists
ADMIN_EMAILS = ["yahya.ouarach@arrow.com", "mafernandez@arrow.com"]
USER_EMAILS = ["nassim.bouzaid@arrow.com"] # Case-insensitive handled by .lower()
ALL_AUTHORIZED = ADMIN_EMAILS + USER_EMAILS

# Styling: High-Contrast Corporate UI (Fixes "Black Button" issue)
st.markdown("""
<style>
    /* Main Background */
    .stApp { background-color: #ffffff; color: #000000; }
    
    /* Result Card Styling */
    .result-card { 
        border: 1px solid #d1d5db; padding: 24px; border-radius: 12px; 
        background-color: #ffffff; margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* Instructions Styling (Lightened) */
    .instructions { 
        background-color: #f9fafb; padding: 18px; border-left: 6px solid #005a9c; 
        white-space: pre-wrap; color: #111827 !important; 
        font-family: 'Consolas', monospace; font-size: 1rem;
        border-radius: 0 8px 8px 0; border-top: 1px solid #e5e7eb;
        border-right: 1px solid #e5e7eb; border-bottom: 1px solid #e5e7eb;
    }

    /* FIX: Button Visibility (No longer black/hidden) */
    .stButton > button {
        background-color: #ffffff !important;
        color: #005a9c !important;
        border: 2px solid #005a9c !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        height: 3em !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        background-color: #005a9c !important;
        color: #ffffff !important;
    }

    /* Admin Badge */
    .admin-badge {
        background-color: #e11d48; color: white; padding: 4px 10px;
        border-radius: 20px; font-size: 0.75rem; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

if 'auth' not in st.session_state:
    st.session_state.auth = False
    st.session_state.user = ""
    st.session_state.is_admin = False

# 2. LOGIN GATE (Fixed Nassim's Access)
if not st.session_state.auth:
    _, center, _ = st.columns([1, 1.5, 1])
    with center:
        st.title("🏹 Arledge Login")
        email_input = st.text_input("Arrow Email Address").lower().strip()
        if st.button("Sign In"):
            if email_input in ALL_AUTHORIZED:
                st.session_state.auth = True
                st.session_state.user = email_input
                st.session_state.is_admin = email_input in ADMIN_EMAILS
                st.rerun()
            else:
                st.error(f"Access Denied: {email_input} is not on the authorized list.")
    st.stop()

# 3. DATA LOADER
@st.cache_data
def load_db():
    file_path = "master_ops_database.csv"
    if os.path.exists(file_path):
        # engine='python' ensures it reads the multi-line instructions correctly
        return pd.read_csv(file_path, engine='python').fillna("")
    return pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale", "File_Source"])

df = load_db()

# 4. SIDEBAR
with st.sidebar:
    st.title("🏹 Arledge")
    role = "ADMIN" if st.session_state.is_admin else "USER"
    st.markdown(f"**{st.session_state.user}** <span class='admin-badge'>{role}</span>", unsafe_allow_html=True)
    
    st.divider()
    page = st.radio("Navigation", ["Knowledge Base", "Admin Dashboard"] if st.session_state.is_admin else ["Knowledge Base"])
    
    st.divider()
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

# 5. PAGE LOGIC
if page == "Knowledge Base":
    st.title("OMT Knowledge Base")
    query = st.text_input("🔍 Search procedures, templates, or contacts...", placeholder="e.g. 'Partial', 'Reno', 'Collector'")

    if query:
        keywords = query.lower().split()
        mask = df.apply(lambda row: all(k in str(row).lower() for k in keywords), axis=1)
        results = df[mask]
        
        if not results.empty:
            st.success(f"Displaying {len(results)} matches")
            for _, row in results.iterrows():
                st.markdown(f"""
                <div class="result-card">
                    <div style="color:#005a9c; font-weight:bold; font-size:0.85rem; text-transform:uppercase;">
                        {row['System']} | {row['File_Source']}
                    </div>
                    <h3 style="margin-top:5px; margin-bottom:15px;">{row['Process']}</h3>
                    <div class="instructions">{row['Instructions']}</div>
                    <div style="margin-top:15px; font-size:0.9rem; color:#4b5563;">
                        <b>Why we do this:</b> {row['Rationale']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No matching procedures found.")
    else:
        st.info("👋 Welcome! Start typing above to search the OMT database.")

# 6. ADMIN DASHBOARD
elif page == "Admin Dashboard":
    st.title("⚙️ Admin Panel")
    
    # Stats Metrics
    m1, m2 = st.columns(2)
    m1.metric("Total SOPs", len(df))
    m2.metric("System Status", "Online / High Contrast")
    
    st.divider()
    st.subheader("Edit Master Database")
    # Live editor for Yahya and Mafernandez
    edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
    
    if st.download_button("💾 Download Updated CSV", data=edited_df.to_csv(index=False), file_name="master_ops_database.csv", mime="text/csv"):
        st.success("CSV ready for download. Please replace your local file with this version.")
