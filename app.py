import streamlit as st
import pandas as pd
import os

# 1. Page Configuration
st.set_page_config(page_title="Arledge Hub", layout="wide")

# 2. Simple Login Logic
def check_password():
    def password_entered():
        if (
            st.session_state["username"] in ["yahya.ouarach@arrow.com", "mafernandez@arrow.com"]
            and st.session_state["password"] == "Arrow2026!"
        ):
            st.session_state["password_correct"] = True
            st.session_state["user_email"] = st.session_state["username"]
            del st.session_state["password"]
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.title("Arledge Hub Login")
        st.text_input("Email", on_change=password_entered, key="username")
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.title("Arledge Hub Login")
        st.text_input("Email", on_change=password_entered, key="username")
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("😕 User not known or password incorrect")
        return False
    return True

if check_password():
    # --- Sidebar Navigation ---
    st.sidebar.title("Navigation")
    
    # Check if the logged-in user is an Admin (Yahya)
    is_admin = st.session_state["user_email"] == "yahya.ouarach@arrow.com"
    
    app_mode = "User View"
    if is_admin:
        app_mode = st.sidebar.radio("Switch Mode", ["User View", "Admin Dashboard"])
    
    st.sidebar.divider()
    if st.sidebar.button("Log out"):
        st.session_state.clear()
        st.rerun()

    # --- Load Data Function ---
    @st.cache_data
    def load_data():
        if os.path.exists("data.csv"):
            return pd.read_csv("data.csv")
        return pd.DataFrame()

    # --- ADMIN DASHBOARD ---
    if app_mode == "Admin Dashboard":
        st.title("🛠️ Admin Dashboard")
        st.subheader("Upload & Update Hub Resources")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Update Database (CSV)")
            uploaded_csv = st.file_uploader("Upload new data.csv", type="csv")
            if uploaded_csv:
                df_new = pd.read_csv(uploaded_csv)
                df_new.to_csv("data.csv", index=False)
                st.success("Database updated successfully!")
                st.cache_data.clear() # Clear cache to show new data immediately

        with col2:
            st.write("### Upload SOPs (PDF)")
            uploaded_pdf = st.file_uploader("Upload SOP PDF", type="pdf")
            if uploaded_pdf:
                # Create a directory for PDFs if it doesn't exist
                if not os.path.exists("sops"):
                    os.makedirs("sops")
                with open(os.path.join("sops", uploaded_pdf.name), "wb") as f:
                    f.write(uploaded_pdf.getbuffer())
                st.success(f"SOP '{uploaded_pdf.name}' uploaded to storage!")

    # --- USER VIEW (The Hub) ---
    else:
        st.title("Arledge Hub")
        df = load_data()

        if not df.empty:
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
                    
                # PDF SOP Link (If exists)
                sop_path = f"sops/{selected_process}.pdf"
                if os.path.exists(sop_path):
                    with open(sop_path, "rb") as f:
                        st.download_button("📂 Download Full SOP PDF", f, file_name=f"{selected_process}.pdf")
            else:
                st.info("Select a process above to begin.")
        else:
            st.warning("No data found. Please use the Admin Dashboard to upload 'data.csv'.")
