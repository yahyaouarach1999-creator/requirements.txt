import streamlit as st
import pandas as pd
import os

# 1. Page Configuration
st.set_page_config(page_title="Arledge Hub", layout="wide")

# 2. Initialize Session State
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False
if "user_email" not in st.session_state:
    st.session_state["user_email"] = ""

# 3. Login Function
def login_page():
    st.title("Arledge Hub Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        # Authorized Users & Password
        if email in ["yahya.ouarach@arrow.com", "mafernandez@arrow.com"] and password == "Arrow2026!":
            st.session_state["password_correct"] = True
            st.session_state["user_email"] = email
            st.rerun() # Refresh to show the app
        else:
            st.error("Invalid email or password")

# 4. Main App Logic
if not st.session_state["password_correct"]:
    login_page()
else:
    # --- Sidebar Navigation ---
    st.sidebar.title("Navigation")
    
    # Check if Admin (Yahya)
    is_admin = st.session_state["user_email"] == "yahya.ouarach@arrow.com"
    
    app_mode = "User View"
    if is_admin:
        app_mode = st.sidebar.radio("Switch Mode", ["User View", "Admin Dashboard"])
    
    st.sidebar.divider()
    if st.sidebar.button("Log out"):
        st.session_state["password_correct"] = False
        st.session_state["user_email"] = ""
        st.rerun()

    # --- Load Data Function ---
    def load_data():
        if os.path.exists("data.csv"):
            try:
                return pd.read_csv("data.csv")
            except Exception as e:
                st.error(f"Error reading data.csv: {e}")
                return pd.DataFrame()
        return pd.DataFrame()

    # --- ADMIN DASHBOARD ---
    if app_mode == "Admin Dashboard":
        st.title("🛠️ Admin Dashboard")
        st.subheader("Update Hub Resources")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Update Database (CSV)")
            uploaded_csv = st.file_uploader("Upload new data.csv", type="csv")
            if uploaded_csv:
                df_new = pd.read_csv(uploaded_csv)
                df_new.to_csv("data.csv", index=False)
                st.success("Database updated! Click 'Rerun' in the menu if data doesn't refresh.")

        with col2:
            st.write("### Upload SOPs (PDF)")
            uploaded_pdf = st.file_uploader("Upload SOP PDF", type="pdf")
            if uploaded_pdf:
                if not os.path.exists("sops"):
                    os.makedirs("sops")
                with open(os.path.join("sops", uploaded_pdf.name), "wb") as f:
                    f.write(uploaded_pdf.getbuffer())
                st.success(f"Uploaded: {uploaded_pdf.name}")

    # --- USER VIEW ---
    else:
        st.title("Arledge Hub")
        df = load_data()

        if not df.empty:
            # Check if columns exist to avoid KeyErrors
            if "Process" in df.columns:
                options = [""] + list(df["Process"].unique())
                selected_process = st.selectbox("🔍 Select a process:", options=options, index=0)

                if selected_process != "":
                    detail = df[df["Process"] == selected_process].iloc[0]
                    
                    st.subheader(f"Details for: {selected_process}")
                    c1, c2 = st.columns(2)
                    with c1:
                        st.info(f"**System:** {detail.get('System', 'N/A')}")
                        st.success(f"**Rationale:** {detail.get('Rationale', 'N/A')}")
                    with c2:
                        st.warning(f"**Instructions:**\n{detail.get('Instructions', 'N/A')}")
                    
                    # PDF Download Link
                    sop_path = f"sops/{selected_process}.pdf"
                    if os.path.exists(sop_path):
                        with open(sop_path, "rb") as f:
                            st.download_button("📂 Download SOP PDF", f, file_name=f"{selected_process}.pdf")
            else:
                st.error("The CSV file is missing a 'Process' column.")
        else:
            st.info("The database is currently empty. Use Admin Mode to upload 'data.csv'.")
