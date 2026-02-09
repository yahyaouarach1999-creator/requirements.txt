Import streamlit as st
import pandas as pd
import re
import io
import urllib.parse
from PyPDF2 import PdfReader
import google.generativeai as genai

# =========================================================
# 1. PAGE SETUP
# =========================================================
st.set_page_config(
    page_title="Arledge Command Center",
    page_icon="🏹",
    layout="wide"
)

# =========================================================
# 2. AI INITIALIZATION (SECURE)
# =========================================================
@st.cache_resource
def init_model():
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        return genai.GenerativeModel("models/gemini-1.5-flash")
    except Exception:
        return None

model = init_model()

# =========================================================
# 3. DATA & HELPERS
# =========================================================
@st.cache_data
def load_data():
    try:
        return pd.read_csv("sop_data.csv").fillna("")
    except Exception:
        df = pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale"])
        df.to_csv("sop_data.csv", index=False)
        return df

@st.cache_data(show_spinner=False)
def extract_pdf_text(file_bytes):
    reader = PdfReader(io.BytesIO(file_bytes))
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def validate_rows(df):
    required = {"System", "Process", "Instructions", "Rationale"}
    return required.issubset(df.columns) and not df.empty

def search_df(df, query):
    mask = (
        df["System"].str.contains(query, case=False) |
        df["Process"].str.contains(query, case=False) |
        df["Instructions"].str.contains(query, case=False) |
        df["Rationale"].str.contains(query, case=False)
    )
    return df[mask]

def highlight(text, query):
    return re.sub(
        f"({re.escape(query)})",
        r"<mark>\1</mark>",
        text,
        flags=re.IGNORECASE
    )

# =========================================================
# 4. STYLES
# =========================================================
st.markdown("""
<style>
.main-header {
    background:#0F172A;
    color:white;
    padding:12px;
    text-align:center;
    border-bottom:3px solid #F97316;
    margin-bottom:15px;
}
.nano-tile {
    background:#F8FAFC;
    border:1px solid #CBD5E1;
    border-radius:8px;
    padding:10px;
    text-align:center;
}
.nano-label {
    font-size:0.7rem;
    font-weight:800;
    color:#64748B;
    text-transform:uppercase;
}
.instruction-box {
    white-space:pre-wrap;
    font-family:monospace;
    background:#1E293B;
    color:#F8FAFC;
    padding:15px;
    border-left:5px solid #F97316;
    border-radius:6px;
}
mark {
    background:#FACC15;
    padding:2px 4px;
    border-radius:4px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 5. AUTH
# =========================================================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<div class="main-header"><h4>🔒 ARROW.COM ACCESS REQUIRED</h4></div>', unsafe_allow_html=True)
    email = st.text_input("Official Arrow Email")
    if st.button("Enter Portal"):
        if "@arrow.com" in email.lower():
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Access denied.")
    st.stop()

# =========================================================
# 6. HEADER
# =========================================================
st.markdown('<div class="main-header"><h4>🏹 ARLEDGE OPERATIONS COMMAND</h4></div>', unsafe_allow_html=True)

# =========================================================
# 7. QUICK NAV
# =========================================================
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown('<div class="nano-tile"><div class="nano-label">Salesforce</div></div>', unsafe_allow_html=True)
    st.link_button("🚀 CRM", "https://arrowcrm.lightning.force.com/", use_container_width=True)

with c2:
    st.markdown('<div class="nano-tile"><div class="nano-label">SWB Oracle</div></div>', unsafe_allow_html=True)
    st.link_button("💾 Orders", "https://acswb.arrow.com/Swb/", use_container_width=True)

with c3:
    st.markdown('<div class="nano-tile"><div class="nano-label">ETQ Portal</div></div>', unsafe_allow_html=True)
    st.link_button("📋 Forms", "https://arrow.etq.com/prod/rel/#/app/system/portal", use_container_width=True)

with c4:
    st.markdown('<div class="nano-tile"><div class="nano-label">ServiceNow</div></div>', unsafe_allow_html=True)
    st.link_button("🛠️ Tickets", "https://arrow.service-now.com/myconnect", use_container_width=True)

with c5:
    st.markdown('<div class="nano-tile"><div class="nano-label">SOS Help</div></div>', unsafe_allow_html=True)
    st.link_button("🆘 Contact", "mailto:yahya.ouarach@arrow.com", use_container_width=True)

st.divider()

# =========================================================
# 8. ADMIN SIDEBAR
# =========================================================
df = load_data()

st.sidebar.title("⚙️ Admin Console")
if st.sidebar.checkbox("🚀 Smart AI Upload"):
    st.sidebar.info("Upload SOP PDF → AI extracts procedures")
    pdf = st.sidebar.file_uploader("Upload PDF", type="pdf")

    if pdf and st.sidebar.button("✨ Extract & Preview"):
        if model is None:
            st.sidebar.error("AI not initialized.")
        else:
            with st.spinner("Reading SOP..."):
                raw_text = extract_pdf_text(pdf.getvalue())
                prompt = f"""
Extract SOP procedures.

Rules:
- Output ONLY CSV rows
- NO markdown
- 4 columns exactly:
System, Process, Instructions, Rationale

TEXT:
{raw_text[:8000]}
"""
                response = model.generate_content(prompt)
                cleaned = response.text.replace("```", "").strip()

                preview_df = pd.read_csv(
                    io.StringIO(cleaned),
                    names=["System", "Process", "Instructions", "Rationale"],
                    on_bad_lines="skip"
                )

                if validate_rows(preview_df):
                    st.sidebar.success(f"Extracted {len(preview_df)} rows")
                    st.session_state.preview_df = preview_df
                else:
                    st.sidebar.error("Extraction failed")

    if "preview_df" in st.session_state:
        if st.sidebar.button("✅ Save to Database"):
            final_df = pd.concat([df, st.session
