# --- 2. THE PERMANENT LOGO FIX (BASE64) ---
LOGO_SVG = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iI0Y5NzMxNiIgZD0iTTEyIDJMMiA3bDEwIDUgMTAtNXYxMEgxMlYyMmw4LTUgNC01Vjd6Ii8+PC9zdmc+"

# Use double {{ }} for CSS inside an f-string
st.markdown(f"""
    <style>
        #MainMenu {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}
        header {{ visibility: hidden; }}
        .stApp {{ background-color: #F8FAFC; }}
        
        .header-container {{
            display: flex;
            align-items: center;
            background-color: #1E293B;
            padding: 15px 25px;
            border-radius: 10px;
            border-bottom: 5px solid #F97316;
            margin-bottom: 20px;
        }}
        .logo-box {{
            background: white;
            padding: 8px;
            border-radius: 5px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .title-text {{
            color: white !important;
            font-size: 40px;
            font-weight: 900;
            margin-left: 20px;
            letter-spacing: 2px;
        }}
        /* Visibility Fix for typing */
        .stTextInput input {{
            color: #000000 !important;
            background-color: #FFFFFF !important;
        }}
        label, p, .stMarkdown {{
            color: #1E293B !important;
        }}
    </style>
    
    <div class="header-container">
        <div class="logo-box">
            <img src="{LOGO_SVG}" width="50">
        </div>
        <div class="title-text">ARLEDGE</div>
    </div>
""", unsafe_allow_html=True)
