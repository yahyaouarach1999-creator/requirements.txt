import streamlit as st
import pandas as pd
import re
import urllib.parse

# --- 1. CONFIG & BRANDING ---
st.set_page_config(page_title="Arledge", layout="wide", page_icon="🏹")

# Add a professional sidebar logo
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Arrow_Electronics_Logo.svg", width=150)
st.sidebar.title("Arledge Navigation")
st.sidebar.markdown("---")

st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #1E293B; }
    .arledge-banner { 
        text-align: center; padding: 30px; 
        background: linear-gradient(90deg, #1E293B 0%, #334155 100%); 
        color: white; border-radius: 15px; margin-bottom: 20px;
    }
    .sop-card { 
        border: 1px solid #E2E8F0; border-radius: 12px; padding: 20px; 
        background: white; margin-bottom: 12px; border-left: 6px solid #F97316;
    }
    .system-badge { background: #1E293B; color: white; padding: 4px 12px; border-radius: 15px; font-size: 11px; font-weight: 700; }
    .verified-badge { color: #10B981; font-weight: bold; font-size: 14px; }
</style>
""", unsafe_allow_html=True)

# --- 2. SECURITY GATE ---
if 'authorized' not in st.session_state: st.session_state.authorized = False

if not st.session_state.authorized:
    st.markdown("<div style='text-align:center; padding-top:100px;'>", unsafe_allow_html=True)
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Arrow_Electronics_Logo.svg", width=250)
    st.title("Arledge Knowledge Terminal")
    pwd = st.text_input("Enter Access Key", type="password")
    if st.button("Unlock Terminal") or (pwd == "Arrow2026"):
        if pwd == "Arrow2026":
            st.session_state.authorized = True
            st.rerun()
        elif pwd != "":
            st.error("Invalid Key")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 3. DATA ENGINE ---
@st.cache_data(ttl=1)
def load_data():
    try:
        df = pd.read_csv("sop_data.csv", encoding='utf-8-sig')
        df.columns = df.columns.str.strip()
        return df.fillna("")
    except:
        return pd.DataFrame()

df = load_data()

# --- 4. PERSISTENT STATE MANAGEMENT ---
if 'view' not in st.session_state: st.session_state.view = 'home'
if 'search_query' not in st.session_state: st.session_state.search_query = ""
if 'search_id' not in st.session_state: st.session_state.search_id = ""

# --- 5. SEARCH HOME PAGE ---
if st.session_state.view == 'home':
    st.markdown("<div class='arledge-banner'><h1>🏹 Arledge Knowledge Terminal</h1></div>", unsafe_allow_html=True)
    
    # Clickable Stat Summary (Visual Only)
    s1, s2, s3 = st.columns(3)
    s1.button(f"📄 {len(df)} Active SOPs", use_container_width=True)
    s2.button(f"⚙️ {len(df['System'].unique())} Systems", use_container_width=True)
    s3.button(f"📧 {len(df[df['Email_Template'] != ''])} Templates", use_container_width=True)
    
    st.write("---")
    
    # PERSISTENT SEARCH INPUT
    query = st.text_input(
        "Search Box", 
        value=st.session_state.search_query, 
        placeholder="Search keywords (e.g. Unity, RMA, Venlo) or enter ID #...", 
        label_visibility="collapsed"
    ).strip()
    
    # Save query to state so it's there when we come back
    st.session_state.search_query = query

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
            st.warning("No matches found.")
    else:
        # Show default items if no search
        st.info("👋 Welcome! Use the search bar above to filter workflows.")
        for idx, row in df.head(3).iterrows():
            st.markdown("<div class='sop-card'>", unsafe_allow_html=True)
            col_a, col_b = st.columns([0.8, 0.2])
            col_a.markdown(f"### {row['Process']}")
            col_a.button("View Details", key=f"pre_{idx}", on_click=lambda r=row: (st.session_state.update({"selected": r, "view": "detail"})))
            st.markdown("</div>", unsafe_allow_html=True)

# --- 6. DETAIL SOP PAGE ---
elif st.session_state.view == 'detail':
    row = st.session_state.selected
    
    # GO BACK BUTTON (Keeps search_query intact)
    if st.button("← Back to Results"):
        st.session_state.view = 'home'
        st.rerun()
    
    st.divider()
    l, r = st.columns([0.6, 0.4])
    
    with l:
        st.markdown(f"<span class='verified-badge'>✅ VERIFIED CONTENT</span>")
        st.title(row['Process'])
        st.write(f"**System:** {row['System']} | **Revised:** {row['Last_Updated']}")
        
        st.subheader("Operational Steps")
        for step in row['Instructions'].split('<br>'):
            st.markdown(f"🔹 {step}")
            
        if row['Email_Template']:
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
            st.image(row['Screenshot_URL'], caption="Reference Screenshot", use_container_width=True)
