import streamlit as st
import pandas as pd
import re
import urllib.parse

# --- 1. SETTINGS ---
st.set_page_config(page_title="Arledge", layout="wide", page_icon="🏹")

# --- 2. THE PERMANENT LOGO FIX (BASE64) ---
LOGO_SVG = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iI0Y5NzMxNiIgZD0iTTEyIDJMMiA3bDEwIDUgMTAtNXYxMEgxMlYyMmw4LTUgNC01Vjd6Ii8+PC9zdmc+"

st.markdown(f"""
    <style>
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        /* Main Background */
        .stApp {{ background-color: #F8FAFC; }}
        
        /* HEADER STYLING */
        .header-container {{
            display: flex;
            align-items: center;
            background-color: #1E293B;
            padding: 15px 25px;
            border-radius: 10px;
            border-bottom: 5px solid #F97316;
            margin-bottom: 20px;
        }
        .logo-box {{
            background: white;
            padding: 8px;
            border-radius: 5px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .title-text {{
            color: white !important;
            font-size: 40px;
            font-weight: 900;
            margin-left: 20px;
            letter-spacing: 2px;
        }

        /* VISIBILITY FIX: Force dark text for inputs and search labels */
        label, p, .stMarkdown, .stTextInput label {{
            color: #1E293B !important;
            font-weight: 600 !important;
        }
        
        /* Force search text to be black so it's visible while typing */
        .stTextInput input {{
            color: #000000 !important;
            background-color: #FFFFFF !important;
        }

        /* Result Cards */
        .result-card {{
            background: white; 
            padding: 15px; 
            border-left: 5px solid #F97316; 
            margin-bottom: 10px; 
            border-radius: 5px; 
            box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        }
    </style>
    
    <div class="header-container">
        <div class="logo-box">
            <img src="{LOGO_SVG}" width="50">
        </div>
        <div class="title-text">ARLEDGE</div>
    </div>
""", unsafe_allow_html=True)

# --- 3. SECURITY GATE ---
if 'authorized' not in st.session_state: st.session_state.authorized = False

if not st.session_state.authorized:
    st.info("🔒 Secure Terminal")
    pwd = st.text_input("Enter Key", type="password")
    if st.button("Unlock") or (pwd == "Arrow2026"):
        if pwd == "Arrow2026":
            st.session_state.authorized = True
            st.rerun()
        elif pwd != "":
            st.error("Invalid")
    st.stop()

# --- 4. DATA ENGINE ---
@st.cache_data(ttl=1)
def load_data():
    try:
        # Changed to sop_data.csv to match Arledge logic
        df = pd.read_csv("sop_data.csv", encoding='utf-8-sig').fillna("")
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Screenshot_URL", "Email_Template", "Last_Updated"])

df = load_data()

# --- 5. SEARCH & VIEW LOGIC ---
if 'view' not in st.session_state: st.session_state.view = 'home'
if 'query' not in st.session_state: st.session_state.query = ""

if st.session_state.view == 'home':
    col1, col2 = st.columns(2)
    col1.metric("Indexed SOPs", len(df))
    col2.metric("Platforms", len(df['System'].unique()) if not df.empty else 0)
    
    # Text input with forced visibility
    query = st.text_input("🔍 Search Database...", value=st.session_state.query, placeholder="Type process name here...").strip()
    st.session_state.query = query

    if query:
        mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
        results = df[mask]
        
        if results.empty:
            st.warning("No results found.")
        else:
            for idx, row in results.iterrows():
                st.markdown(f"""
                <div class="result-card">
                    <small style="color:#F97316; font-weight:bold;">{row['System']}</small>
                    <h4 style="margin:0; color:#1E293B;">{row['Process']}</h4>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Open {row['Process']}", key=f"v_{idx}"):
                    st.session_state.selected = row
                    st.session_state.view = 'detail'
                    st.rerun()
    else:
        st.write("### Ready. Type to search.")

elif st.session_state.view == 'detail':
    row = st.session_state.selected
    if st.button("← Back"):
        st.session_state.view = 'home'
        st.rerun()
    
    st.divider()
    l, r = st.columns([0.6, 0.4])
    
    with l:
        st.title(row['Process'])
        st.write(f"**Platform:** `{row['System']}`")
        st.markdown("### 📋 Steps")
        # Split by <br> or newline
        steps = row['Instructions'].replace('<br>', '\n').split('\n')
        for step in steps:
            if step.strip():
                st.markdown(f"✅ {step.strip()}")
            
        if row['Email_Template']:
            st.divider()
            st.subheader("📧 Smart Template")
            num_match = re.search(r'\d+', st.session_state.query)
            id_val = num_match.group(0) if num_match else "[ID]"
            full_tpl = row['Email_Template'].replace("[NUMBER]", id_val)
            
            parts = full_tpl.split('\n', 1)
            subject = parts[0].replace("Subject: ", "") if parts else "Update"
            body = parts[1] if len(parts) > 1 else full_tpl
            
            st.info(f"**Subject:** {subject}")
            st.code(body, language="text")
            
            mailto = f"mailto:?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
            st.markdown(f'<a href="{mailto}" style="background:#F97316;color:white;padding:12px;text-decoration:none;border-radius:5px;font-weight:bold;">🚀 Launch Outlook</a>', unsafe_allow_html=True)

    with r:
        if row['Screenshot_URL']:
            st.image(row['Screenshot_URL'], caption="Process Visualization")
