import streamlit as st
import pandas as pd
import os
import re

# 1. PAGE SETUP
st.set_page_config(page_title="Arledge", layout="wide", page_icon="🏹")

# Initialize Theme State
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Function to toggle theme
def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

# --- AUTHORIZATION LIST ---
ADMIN_EMAILS = ["yahya.ouarach@arrow.com", "mafernandez@arrow.com"]
USER_EMAILS = ["nassim.bouzaid@arrow.com"]
ALL_AUTHORIZED = ADMIN_EMAILS + USER_EMAILS

# 2. DYNAMIC STYLING (Light/Dark Mode)
if st.session_state.dark_mode:
    # DARK MODE COLORS
    bg_color = "#0e1117"
    text_color = "#ffffff"
    card_bg = "#1f2937"
    border_color = "#374151"
    input_bg = "#262730"
else:
    # LIGHT MODE COLORS
    bg_color = "#ffffff"
    text_color = "#1f2937"
    card_bg = "#f9fafb"
    border_color = "#e5e7eb"
    input_bg = "#ffffff"

st.markdown(f"""
<style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    
    /* Search Bar Adjustment */
    .stTextInput input {{
        background-color: {input_bg} !important;
        color: {text_color} !important;
        border: 2px solid #005a9c !important;
        border-radius: 8px !important;
    }}
    
    /* Global Text Colors */
    h1, h2, h3, h4, p, span, label {{ color: {text_color} !important; }}

    /* Action Buttons */
    div.stButton > button {{
        background-color: {bg_color} !important;
        color: #005a9c !important;
        border: 2px solid #005a9c !important;
        font-weight: bold !important;
    }}
    div.stButton > button:hover {{
        background-color: #005a9c !important;
        color: #ffffff !important;
    }}

    /* Accordion / Expander */
    .st-expander {{
        border: 1px solid {border_color} !important;
        border-radius: 10px !important;
        background-color: {card_bg} !important;
        margin-bottom: 12px !important;
    }}

    .admin-badge {{
        background-color: #be185d; color: white; padding: 2px 10px;
        border-radius: 12px; font-size: 0.7rem; font-weight: bold;
    }}
</style>
""", unsafe_allow_html=True)

# Helper function to clean and organize rules
def format_rules(text):
    steps = re.split(r'(?:\d+\.|\n-|\n\*)', text)
    if len(steps) > 1:
        formatted = ""
        count = 1
        for s in steps:
            clean_s = s.strip()
            if clean_s:
                formatted += f"**Rule {count}:** {clean_s}  \n"
                count += 1
        return formatted
    return text

if 'auth' not in st.session_state:
    st.session_state.auth = False
    st.session_state.user = ""
    st.session_state.is_admin = False

# 3. LOGIN GATE
if not st.session_state.auth:
    _, center, _ = st.columns([1, 1.5, 1])
    with center:
        st.title("🏹 Arledge Login")
        email_input = st.text_input("Arrow Email Address").lower().strip()
        if st.button("Sign In", use_container_width=True):
            if email_input in ALL_AUTHORIZED:
                st.session_state.auth = True
                st.session_state.user = email_input
                st.session_state.is_admin = (email_input in ADMIN_EMAILS)
                st.rerun()
            else:
                st.error(f"Access Denied: {email_input} is not authorized.")
    st.stop()

# 4. DATA LOADER
@st.cache_data
def load_db():
    file_path = "master_ops_database.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path, engine='python').fillna("")
    return pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale", "File_Source"])

df = load_db()

# 5. SIDEBAR
with st.sidebar:
    st.title("🏹 Arledge")
    
    # THEME TOGGLE BUTTON
    theme_label = "☀️ Light Mode" if st.session_state.dark_mode else "🌙 Dark Mode"
    if st.button(theme_label, use_container_width=True):
        toggle_theme()
        st.rerun()

    st.divider()
    role = "ADMIN" if st.session_state.is_admin else "USER"
    st.markdown(f"**{st.session_state.user}** <span class='admin-badge'>{role}</span>", unsafe_allow_html=True)
    
    st.divider()
    page = st.radio("Navigation", ["Knowledge Base", "Admin Dashboard"] if st.session_state.is_admin else ["Knowledge Base"])
    
    st.divider()
    st.markdown("### ⚡ Quick Access Links")
    st.markdown("• [☁️ Oracle Unity](https://acerpebs.arrow.com/OA_HTML/RF.jsp?function_id=16524)")
    st.markdown("• [🚩 Salesforce](https://arrowcrm.lightning.force.com/)")
    st.markdown("• [💻 SWB Dashboard](https://acswb.arrow.com/Swb/)")
    st.markdown("• [📋 ETQ Portal](https://arrow.etq.com/prod/rel/#/app/auth/login)")
    st.markdown("• [🛠 MyConnect IT](https://arrow.service-now.com/myconnect)")
    
    if st.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# 6. KNOWLEDGE BASE
if page == "Knowledge Base":
    st.title("Knowledge Base")
    query = st.text_input("🔍 Search Rules & Processes", placeholder="e.g. 'Partial', 'Venlo', 'Credit'")

    if query:
        keywords = query.lower().split()
        mask = df.apply(lambda row: all(k in str(row).lower() for k in keywords), axis=1)
        results = df[mask]
        
        if not results.empty:
            st.write(f"Showing {len(results)} matches:")
            for _, row in results.iterrows():
                with st.expander(f"⚙️ {row['System']} ▸ {row['Process']}", expanded=False):
                    st.markdown("### 📋 Rules & Procedures")
                    st.markdown(format_rules(row['Instructions']))
        else:
            st.warning("No matches found.")
    else:
        st.info("👋 Enter a keyword to display specific rules and processes.")

# 7. ADMIN DASHBOARD
elif page == "Admin Dashboard":
    st.title("⚙️ Admin Panel")
    st.subheader("Master Database Management")
    
    edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
    
    if st.download_button("💾 Save Changes (CSV)", data=edited_df.to_csv(index=False), file_name="master_ops_database.csv", mime="text/csv"):
        st.success("Changes saved. Download the file and update your repository.")
