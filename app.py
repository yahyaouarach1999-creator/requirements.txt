import streamlit as st
import pandas as pd
import re
import urllib.parse

# --- 1. CONFIG & ARLEDGE BRANDING ---
st.set_page_config(page_title="Arledge Knowledge Terminal", layout="wide", page_icon="🏹")

st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; }
    .arledge-banner { 
        text-align: center; padding: 40px; 
        background: linear-gradient(90deg, #1E293B 0%, #334155 100%); 
        color: white; border-radius: 15px; margin-bottom: 25px;
    }
    .stat-box {
        background: #F8FAFC; padding: 15px; border-radius: 10px;
        text-align: center; border-bottom: 4px solid #F97316;
    }
    .sop-card { 
        border: 1px solid #E2E8F0; border-radius: 12px; padding: 20px; 
        background: white; margin-bottom: 12px; border-left: 6px solid #F97316;
        transition: 0.2s;
    }
    .sop-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    .system-badge { background: #1E293B; color: white; padding: 4px 12px; border-radius: 15px; font-size: 11px; font-weight: 700; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 2. THE SECURITY GATE ---
if 'authorized' not in st.session_state: st.session_state.authorized = False

if not st.session_state.authorized:
    st.markdown("<div style='text-align:center; padding-top:100px;'>", unsafe_allow_html=True)
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Arrow_Electronics_Logo.svg", width=250)
    st.title("Arledge Knowledge Terminal")
    pwd = st.text_input("Enter Access Key", type="password")
    if st.button("Unlock Terminal"):
        if pwd == "Arrow2026":
            st.session_state.authorized = True
            st.rerun()
        else:
            st.error("Invalid Key")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 3. DATA ENGINE ---
@st.cache_data(ttl=1)
def load_arledge_data():
    try:
        df = pd.read_csv("sop_data.csv", encoding='utf-8-sig')
        df.columns = df.columns.str.strip()
        # Ensure 'Last_Updated' exists, if not, add a default
        if 'Last_Updated' not in df.columns:
            df['Last_Updated'] = "Verified 2026"
        return df.fillna("")
    except:
        return pd.DataFrame()

df = load_arledge_data()

# --- 4. NAVIGATION & STATE ---
if 'view' not in st.session_state: st.session_state.view = 'home'
if 'search_id' not in st.session_state: st.session_state.search_id = ""

# --- 5. SEARCH HOME PAGE ---
if st.session_state.view == 'home':
    st.markdown("<div class='arledge-banner'><h1>🏹 Arledge Knowledge Terminal</h1><p>Arrow Electronics Operations Repository</p></div>", unsafe_allow_html=True)
    
  # --- 4. SUMMARY DASHBOARD (INTERACTIVE) ---
if st.session_state.view == 'home':
    st.markdown("<div class='arledge-banner'><h1>🏹 Arledge Knowledge Summary</h1></div>", unsafe_allow_html=True)
    
    # Dashboard Stats as CLICKABLE BUTTONS
    s1, s2, s3 = st.columns(3)
    
    with s1:
        if st.button(f"📄 {len(df)} Active SOPs"):
            st.session_state.filter = "all"
            
    with s2:
        if st.button(f"⚙️ {len(df['System'].unique())} Systems Indexed"):
            st.session_state.filter = "systems"
            
    with s3:
        if st.button(f"📧 {len(df[df['Email_Template'] != ''])} Smart Templates"):
            st.session_state.filter = "templates"

    st.write("---")

    if query:
        nums = re.findall(r'\d+', query)
        if nums: st.session_state.search_id = nums[0]

        mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
        results = df[mask]
        
        if not results.empty:
            for idx, row in results.iterrows():
                st.markdown("<div class='sop-card'>", unsafe_allow_html=True)
                col_a, col_b = st.columns([0.8, 0.2])
                col_a.markdown(f"### {row['Process']}")
                col_a.markdown(f"<span class='system-badge'>{row['System']}</span> | Updated: `{row['Last_Updated']}`", unsafe_allow_html=True)
                if col_b.button("View Details", key=f"btn_{idx}"):
                    st.session_state.selected = row
                    st.session_state.view = 'detail'
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("No matches found in Arledge Knowledge base.")
    else:
        st.info("👋 Welcome! Use the search bar above to access Arledge operational workflows.")

# --- 6. DETAIL SOP PAGE ---
elif st.session_state.view == 'detail':
    row = st.session_state.selected
    if st.button("← Back to Arledge Home"):
        st.session_state.view = 'home'
        st.rerun()
    
    st.divider()
    l, r = st.columns([0.6, 0.4])
    
    with l:
        st.title(row['Process'])
        st.write(f"**System:** {row['System']} | **Revised:** {row['Last_Updated']}")
        
        st.subheader("Operational Steps")
        steps = row['Instructions'].split('<br>')
        for step in steps:
            st.markdown(f"🔹 {step}")
            
        if "Email_Template" in row and row['Email_Template']:
            st.divider()
            st.subheader("📧 Smart Email Template")
            id_fill = st.session_state.search_id if st.session_state.search_id else "[ID]"
            final_tpl = row['Email_Template'].replace("[NUMBER]", id_fill)
            st.text_area("Live Template:", value=final_tpl, height=180)
            
            sub = final_tpl.split('\n')[0].replace("Subject: ", "")
            body = "\n".join(final_tpl.split('\n')[1:])
            mailto = f"mailto:?subject={urllib.parse.quote(sub)}&body={urllib.parse.quote(body)}"
            st.markdown(f'<a href="{mailto}" style="background:#F97316;color:white;padding:12px 24px;text-decoration:none;border-radius:8px;font-weight:bold;display:inline-block;">🚀 Open in Outlook</a>', unsafe_allow_html=True)

    with r:
        if row['Screenshot_URL']:
            st.markdown("### Visual Reference")
            st.image(row['Screenshot_URL'], use_container_width=True)
