import streamlit as st
import pandas as pd
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import re
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Arledge", page_icon="🏹", layout="wide")

# --- LOAD USERS & AUTHENTICATION ---
if not os.path.exists("users.yaml"):
    st.error("Please create a 'users.yaml' file to continue.")
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

# --- LOGIN WIDGET ---
# Returns name, authentication_status, and username
name, authentication_status, username = authenticator.login(location='main')

if st.session_state.get("authentication_status") is False:
    st.error("Username/password is incorrect")

elif st.session_state.get("authentication_status") is None:
    st.warning("Please enter your credentials")

elif st.session_state.get("authentication_status"):
    # --- AUTHENTICATED CONTENT ---
    authenticator.logout("Logout", "sidebar")
    
    st.sidebar.title("🏹 Arledge")
    st.sidebar.write(f"Welcome **{st.session_state['name']}**")

    page = st.sidebar.radio("Navigation", ["Knowledge Base", "Admin Dashboard"])

    # --- DATABASE LOADING ---
    @st.cache_data
    def load_data():
        if os.path.exists("master_ops_database.csv"):
            return pd.read_csv("master_ops_database.csv").fillna("")
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale", "File_Source"])

    df = load_data()

    # --- HELPER: RULE FORMATTER ---
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

    # --- HELPER: SEARCH ---
    def search(query):
        keywords = query.lower().split()
        mask = df.apply(lambda row: all(k in str(row).lower() for k in keywords), axis=1)
        return df[mask]

    # --- PAGE: KNOWLEDGE BASE ---
    if page == "Knowledge Base":
        st.title("Knowledge Base")
        query = st.text_input("Search process", placeholder="ex: credit venlo partial")

        if query:
            results = search(query)
            st.write(f"{len(results)} results found")
            for _, row in results.iterrows():
                with st.expander(f"{row['System']} ▸ {row['Process']}"):
                    st.markdown("### Instructions")
                    st.markdown(format_rules(row["Instructions"]))
                    if "Rationale" in row and row["Rationale"]:
                        st.info(f"**Rationale:** {row['Rationale']}")
        else:
            st.info("Enter keywords to search")

    # --- PAGE: ADMIN DASHBOARD ---
    if page == "Admin Dashboard":
        st.title("Admin Dashboard")
        edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic", key="db_editor")

        if st.button("Save Changes"):
            edited_df.to_csv("master_ops_database.csv", index=False)
            st.cache_data.clear()
            st.success("Database Updated")
            st.rerun()

# --- OPTIONAL: HASH GENERATOR TOOL ---
# Uncomment the lines below if you need to generate a new hash for your YAML file
# st.divider()
# if st.checkbox("Show Hash Generator"):
#     pw_to_hash = st.text_input("Enter password to hash", type="password")
#     if pw_to_hash:
#         hashed = stauth.Hasher([pw_to_hash]).generate()
#         st.code(hashed[0], language="text")
#         st.info("Copy this hash into your users.yaml file")
