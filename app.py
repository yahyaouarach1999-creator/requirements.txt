import streamlit as st
import pandas as pd
import os

# 1. PAGE SETUP
st.set_page_config(page_title="Arledge", layout="wide", page_icon="🏹")

# --- IMPROVED ACCESS CONTROL ---
# Combined lists correctly to prevent overwriting
ADMIN_EMAILS = ["yahya.ouarach@arrow.com", "mafernandez@arrow.com"]
USER_EMAILS = ["Nassim.Bouzaid@arrow.com"]
ALL_AUTHORIZED = ADMIN_EMAILS + USER_EMAILS

# Styling: High-End Corporate UI
st.markdown("""
<style>
    .stApp { background-color: #ffffff; color: #000000; }
    .result-card { 
        border: 1px solid #e1e4e8; padding: 24px; border-radius: 12px; 
        background-color: #ffffff; margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        transition: transform 0.2s;
    }
    .result-card:hover { border-color: #005a9c; box-shadow: 0 6px 12px rgba(0,0,0,0.05); }
    .instructions { 
        background-color: #f8f9fa; padding: 18px; border-left: 6px solid #005a9c; 
        white-space: pre-wrap; color: #1a1a1a !important; 
        font-family: 'Consolas', 'Monaco', monospace; font-size: 0.95rem;
        border-radius: 0 8px 8px 0; margin-top: 10px;
    }
    .admin-badge {
        background-color: #dc3545; color: white; padding: 3px 10px;
        border-radius: 20px; font-size: 0.7rem; font-weight: 800; letter-spacing: 0.5px;
    }
    .system-tag {
        background-color: #eef4ff; color: #005a9c; padding: 4px 12px;
        border-radius: 15px; font-size: 0.75rem; font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

if 'auth' not in st.session_state:
    st.session_state.auth = False
    st.session_state.user = ""
    st.session_state.is_admin = False

# 2. LOGIN GATE (Improved centered layout)
if not st.session_state.auth:
    _, center, _ = st.columns([1, 1.5, 1])
    with center:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Arrow_Electronics_logo.svg/1280px-Arrow_Electronics_logo.svg.png", width=200)
        st.title("🏹 Arledge Hub")
        email_input = st.text_input("Enter Arrow Email").lower().strip()
        if st.button("Sign In", use_container_width=True):
            if email_input in ALL_AUTHORIZED:
                st.session_state.auth = True
                st.session_state.user = email_input
                st.session_state.is_admin = email_input in ADMIN_EMAILS
                st.rerun()
            else:
                st.error("Access Denied: Email not in authorized whitelist.")
    st.stop()

# 3. DATA LOADER (Optimized)
@st.cache_data
def load_db():
    file_path = "master_ops_database.csv"
    if os.path.exists(file_path):
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
    st.markdown("### 🛠 Tools")
    st.markdown("• [Oracle Unity](https://acerpebs.arrow.com/OA_HTML/RF.jsp?function_id=16524)")
    st.markdown("• [Salesforce](https://arrowcrm.lightning.force.com/)")
    st.markdown("• [SWB Dashboard](https://acswb.arrow.com/Swb/)")
    
    if st.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# 5. SEARCH LOGIC (Multi-word support)
if page == "Knowledge Base":
    st.title("OMT Knowledge Base")
    query = st.text_input("Search (e.g., 'Partial Ship', 'Venlo', 'Daniel')...", placeholder="What are you looking for today?")

    if query:
        keywords = query.lower().split()
        # Checks if all keywords exist somewhere in the row
        mask = df.apply(lambda row: all(k in str(row).lower() for k in keywords), axis=1)
        results = df[mask]
        
        if not results.empty:
            st.success(f"Found {len(results)} matches for '{query}'")
            for _, row in results.iterrows():
                st.markdown(f"""
                <div class="result-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span class="system-tag">{row['System']}</span>
                        <small style="color:gray;">{row['File_Source']}</small>
                    </div>
                    <h3 style="margin: 10px 0; color:#1a1a1a;">{row['Process']}</h3>
                    <div class="instructions">{row['Instructions']}</div>
                    <div style="margin-top:15px; font-size:0.9rem;">
                        <b>Logic/Rationale:</b> {row['Rationale']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No procedures found for that keyword.")
    else:
        st.info("👋 Welcome! Use the search bar to find SOPs, contacts, and email templates.")

# 6. ADMIN DASHBOARD (New Editable Feature)
elif page == "Admin Dashboard":
    st.title("⚙️ Admin Control Panel")
    
    # KPIs
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Database Entries", len(df))
    kpi2.metric("System Health", "Optimal")
    kpi3.metric("Search Relevancy", "High")

    st.divider()
    st.subheader("Live Database Editor")
    st.write("Changes made below can be downloaded and used to update your local CSV.")
    
    # Advanced Data Editor
    edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
    
    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        st.download_button(
            "💾 Export Edited CSV",
            data=edited_df.to_csv(index=False),
            file_name="master_ops_database.csv",
            mime="text/csv",
            use_container_width=True
        )
    with col_b:
        if st.button("♻️ Clear Cache", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
