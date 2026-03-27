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

# Initialize the authenticator
# Note: Ensure your users.yaml structure matches the expected format
authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"]
)

# --- LOGIN WIDGET ---
# In latest versions, .login() does not return 3 variables. 
# It updates st.session_state automatically.
authenticator.login(location='main')

# --- AUTHENTICATION LOGIC ---
if st.session_state.get("authentication_status") is False:
    st.error("Username/password is incorrect")

elif st.session_state.get("authentication_status") is None:
    st.warning("Please enter your credentials")

elif st.session_state.get("authentication_status"):
    # --- LOGOUT & SIDEBAR ---
    authenticator.logout("Logout", "sidebar")
    
    # Access user details from session state safely
    user_name = st.session_state.get("name", "User")
    st.sidebar.title("🏹 Arledge")
    st.sidebar.write(f"Welcome **{user_name}**")

    page = st.sidebar.radio(
        "Navigation",
        ["Knowledge Base", "Admin Dashboard"]
    )

    # --- LOAD DATABASE ---
    @st.cache_data
    def load_data():
        if os.path.exists("master_ops_database.csv"):
            # Load CSV and fill NaNs with empty strings
            return pd.read_csv("master_ops_database.csv").fillna("")
        # Return empty template if file doesn't exist
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale", "File_Source"])

    df = load_data()

    # --- HELPER: RULE FORMATTER ---
    def format_rules(text):
        # Splitting by numbers (1.), dashes (-), or bullets (*)
        steps = re.split(r'(?:\d+\.|\n-|\n\*)', str(text))
        formatted = ""
        count = 1
        for s in steps:
            s = s.strip()
            if s:
                formatted += f"**Rule {count}:** {s}\n\n"
                count += 1
        return formatted

    # --- HELPER: SEARCH FUNCTION ---
    def search(query):
        keywords = query.lower().split()
        mask = df.apply(
            lambda row: all(
                k in str(row).lower() for k in keywords
            ),
            axis=1
        )
        return df[mask]

    # --- PAGE: KNOWLEDGE BASE ---
    if page == "Knowledge Base":
        st.title("Knowledge Base")
        query = st.text_input("Search process", placeholder="ex: credit venlo partial")

        if query:
            results = search(query)
            st.write(f"{len(results)} results found")
            if not results.empty:
                for _, row in results.iterrows():
                    # Expander for each process found
                    with st.expander(f"{row['System']} ▸ {row['Process']}"):
                        st.markdown("### Instructions")
                        st.markdown(format_rules(row.get("Instructions", "")))
                        if "Rationale" in row and row["Rationale"]:
                            st.info(f"**Rationale:** {row['Rationale']}")
            else:
                st.warning("No results found")
        else:
            st.info("Enter keywords to search")

    # --- PAGE: ADMIN DASHBOARD ---
    if page == "Admin Dashboard":
        st.title("Admin Dashboard")
        
        # Interactive data editor
        edited_df = st.data_editor(
            df,
            use_container_width=True,
            num_rows="dynamic",
            key="db_editor"
        )

        if st.button("Save Changes"):
            edited_df.to_csv("master_ops_database.csv", index=False)
            st.cache_data.clear()
            st.success("Database Updated Successfully!")
            st.rerun()

        st.divider()
        st.subheader("Bulk Import")
        uploaded = st.file_uploader("Upload new database CSV", type=["csv"])
        if uploaded:
            new_df = pd.read_csv(uploaded)
            if st.button("Import & Overwrite Database"):
                new_df.to_csv("master_ops_database.csv", index=False)
                st.cache_data.clear()
                st.success("New database imported and saved")
                st.rerun()

# --- DEVELOPER TOOL: HASH GENERATOR ---
# If you need to generate a password hash for your users.yaml:
with st.sidebar:
    st.divider()
    if st.checkbox("🔑 Hash Generator Tool"):
        st.write("Enter a password to get its hash for users.yaml")
        plain_password = st.text_input("Password to hash", type="password")
        if plain_password:
            # Generate the list of hashes
            hashed_pw = stauth.Hasher([plain_password]).generate()
            st.code(hashed_pw[0], language="text")
            st.caption("Copy this into the password field in users.yaml")
