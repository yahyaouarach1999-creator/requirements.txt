import streamlit as st
import pandas as pd
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import re
import os

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Arledge", page_icon="🏹", layout="wide")

# --- 2. LOAD AUTHENTICATION CONFIG ---
if not os.path.exists("users.yaml"):
    st.error("Missing 'users.yaml' file.")
    st.stop()

with open("users.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initialize Authenticator
authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"]
)

# --- 3. LOGIN WIDGET ---
# Updated for v0.3.x: Handles state internally
authenticator.login(location='main')

# --- 4. AUTHENTICATION CHECK ---
if st.session_state.get("authentication_status") is False:
    st.error("Username/password is incorrect")

elif st.session_state.get("authentication_status") is None:
    st.warning("Please enter your credentials")

elif st.session_state.get("authentication_status"):
    # --- LOGOUT & SIDEBAR ---
    authenticator.logout("Logout", "sidebar")
    
    user_name = st.session_state.get("name", "User")
    st.sidebar.title("🏹 Arledge")
    st.sidebar.write(f"Welcome **{user_name}**")

    page = st.sidebar.radio("Navigation", ["Knowledge Base", "Admin Dashboard"])

    # --- 5. DATABASE LOGIC ---
    @st.cache_data
    def load_data():
        if os.path.exists("master_ops_database.csv"):
            return pd.read_csv("master_ops_database.csv").fillna("")
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale", "File_Source"])

    df = load_data()

    def format_rules(text):
        steps = re.split(r'(?:\d+\.|\n-|\n\*)', str(text))
        formatted = ""
        count = 1
        for s in steps:
            s = s.strip()
            if s:
                formatted += f"**Rule {count}:** {s}\n\n"
                count += 1
        return formatted

    def search(query):
        keywords = query.lower().split()
        mask = df.apply(lambda row: all(k in str(row).lower() for k in keywords), axis=1)
        return df[mask]

    # --- 6. PAGES ---
    if page == "Knowledge Base":
        st.title("Knowledge Base")
        query = st.text_input("Search process", placeholder="ex: credit venlo")

        if query:
            results = search(query)
            st.write(f"{len(results)} results found")
            for _, row in results.iterrows():
                with st.expander(f"{row['System']} ▸ {row['Process']}"):
                    st.markdown("### Instructions")
                    st.markdown(format_rules(row.get("Instructions", "")))
                    if "Rationale" in row and row["Rationale"]:
                        st.info(f"**Rationale:** {row['Rationale']}")
        else:
            st.info("Enter keywords to search")

    if page == "Admin Dashboard":
        st.title("Admin Dashboard")
        edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic", key="db_editor")

        if st.button("Save Changes"):
            edited_df.to_csv("master_ops_database.csv", index=False)
            st.cache_data.clear()
            st.success("Database Updated!")
            st.rerun()

# --- 7. FIXED HASH GENERATOR ---
with st.sidebar:
    st.divider()
    if st.checkbox("🔑 Debug: Generate New Hash"):
        new_pw = st.text_input("Type password to hash", type="password")
        if new_pw:
            # FIXED: Correct syntax for current stauth version
            hashed = stauth.Hasher.hash(new_pw)
            st.code(hashed, language="text")
            st.caption("Copy this into users.yaml")
